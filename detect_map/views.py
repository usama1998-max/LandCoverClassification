import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Images, ImageSegment, ImageSimilarity
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import tensorflow as tf
import cv2
from django.core.paginator import Paginator
import numpy as np
from skimage.metrics import structural_similarity as ssim
from requests import get
from bs4 import BeautifulSoup


trained_model = tf.keras.models.load_model("./modal/landcover_classifier")


project_path = settings.BASE_DIR


classes = [
    'AnnualCrop',
    'Forest',
    'HerbaceousVegetation',
    'Highway',
    'Industrial',
    'Pasture',
    'PermanentCrop',
    'Residential',
    'River',
    'SeaLake'
]


def image_similarity(img1, img2, username):
    # Load two images from different time periods
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)

    sift = cv2.SIFT.create()

    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    # Match keypoints between the two images
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.80 * n.distance:
            good_matches.append(m)

    # Calculate the homography matrix to align the images
    if len(good_matches) > 4:
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        result = cv2.warpPerspective(image1, M, (image2.shape[1], image2.shape[0]))

    # Perform change detection by subtracting the aligned images
    change_map = cv2.absdiff(result, image2)

    # Threshold and identify changes
    threshold = 30
    change_mask = cv2.threshold(change_map, threshold, 255, cv2.THRESH_BINARY)[1]

    # You can further process the change_mask to identify specific changes or areas of interest
    rimage1 = cv2.resize(change_mask, (500, 300))

    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    rgi1 = cv2.resize(gray_image1, (500, 300))
    rgi2 = cv2.resize(gray_image2, (500, 300))

    # Calculate SSIM score
    ssim_score = ssim(rgi1, rgi2)

    file_path = img1.split('/')
    filename = file_path[-1].split('.')[0]
    img_path = f"/{filename}_{username}.png"

    cv2.imwrite("./media/user_imgs_similarity"+img_path, rimage1)

    return ["./user_imgs_similarity"+img_path, round(ssim_score, 2)]


def segment_image(img_url, username):
    # load image as greyscale
    img = cv2.imread(img_url, 0)

    rimg = cv2.resize(img, (500, 500))

    _, river_th = cv2.threshold(rimg, 200, 255, cv2.THRESH_BINARY_INV)
    _, crop_th = cv2.threshold(rimg, 90, 100, cv2.THRESH_BINARY_INV)
    _, vege_th1 = cv2.threshold(rimg, 80, 90, cv2.THRESH_BINARY_INV)

    # gets the labels and the amount of labels, label 0 is the background
    _, label_river = cv2.connectedComponents(river_th)
    _, label_crop = cv2.connectedComponents(crop_th)
    _, label_vege1 = cv2.connectedComponents(vege_th1)

    # lets draw it for visualization purposes
    preview1 = np.zeros((rimg.shape[0], rimg.shape[1], 3), dtype=np.uint8)

    # # draw label 1 blue and label 2 green
    preview1[label_river == 1] = (0, 0, 255)
    preview1[label_crop == 0] = (0, 255, 0)
    preview1[label_vege1 == 2] = (255, 0, 0)

    file_path = img_url.split('/')
    filename = file_path[-1].split('.')[0]
    print("Working on segment...")

    seg_img = f"/{filename}_{username}.png"

    cv2.imwrite("./media/user_imgs_segment"+seg_img, preview1)

    return "/user_imgs_segment"+seg_img


def classify_image(img_url):
    sample = cv2.imread(img_url)
    sample = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)
    nsam = tf.image.resize(sample, (128, 128))
    prediction = trained_model.predict(np.expand_dims(nsam / 255, 0))
    label = np.argmax(prediction)
    return classes[int(label)]


def check_user_email(email: str) -> bool:
    try:
        User.objects.get(email=email)
        return True
    except ObjectDoesNotExist:
        return False


def home(request):
    request.session['dash_panel'] = "0"
    request.session.modified = True
    return render(request, "home.html", {"title": "Home"})


def register(request):
    cuf = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            if check_user_email(form.cleaned_data['email']) is True:
                messages.error(request, "Email already exists")
            else:
                form.save()

                messages.success(request, "Your account has been created, you can now login.")
                return redirect('signin')
        else:
            messages.error(request, form.errors)

    return render(request, "signup.html", {
                                                                "title": "Signup",
                                                                "uform": cuf
                                                               })


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect!")

    return render(request, "signin.html", {"title": "Signin"})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out")
    return redirect('home')


def profile(request):
    return render(request, "profile.html", {"title": f"Welcome {request.user.username}"})


def dashboard(request):
    imgs = None
    page = None
    image_classification = None
    image_feature = None
    one_dim_array = None

    try:
        imgs = Images.objects.filter(user=request.user)
        paginator = Paginator(imgs, 12)
        page_no = request.GET.get('page')
        page = paginator.get_page(page_no)
    except Exception as e:
        print(e)

    try:
        img_class = Images.objects.get(id=int(request.session['img_class_id']))

        if 'img_pred' in request.session:
            image_classification = request.session['img_pred']

    except Exception as e:
        print(f"Image Classification Error: {e}")
        img_class = None
        image_classification = None

    try:
        print(request.session["img_seg_id"])
        img_seg = Images.objects.get(id=int(request.session['img_seg_id']))
    except ObjectDoesNotExist:
        print("Object does not Exist!")
        img_seg = None
    except Exception as e:
        print(e)
        img_seg = None

    try:
        image_seg_result = ImageSegment.objects.get(img_id=img_seg)
    except ObjectDoesNotExist:
        image_seg_result = None
        print("No image found for segements")

    try:
        similar_image = Images.objects.get(id=int(request.session['img_sim']))
    except ObjectDoesNotExist:
        print("Object does not Exist!")
        similar_image = None
    except Exception as e:
        print(e)
        similar_image = None

    try:
        similar_image_result = ImageSimilarity.objects.get(img1=similar_image)
    except ObjectDoesNotExist:
        print("Object does not Exist!")
        similar_image_result = None
    except Exception as e:
        print(e)
        similar_image_result = None

    try:
        print(request.session["image_feature"])
        image_feature = Images.objects.get(id=int(request.session['image_feature']))
    except ObjectDoesNotExist:
        print("Object does not Exist!")
        image_feature = None
    except Exception as e:
        print(e)
        image_feature = None

    if request.method == 'POST':
        print(request.POST)

        if 'dash_panel' in request.POST:
            request.session['dash_panel'] = request.POST['dash_panel']
            request.session.modified = True
            return JsonResponse({"dash_panel": request.session['dash_panel']})

        if 'upload_img' in request.POST:

            if len(request.FILES) > 0:

                user = User.objects.get(username=request.user.username)

                img = Images()
                img.img = request.FILES['img']
                img.user = user
                img.save()
                print("Image Uploaded")

                if "upload_img_class" in request.POST:
                    request.session['img_class_id'] = img.pk
                    request.session.modified = True

                if "upload_img_segment" in request.POST:
                    request.session['img_seg_id'] = img.pk
                    request.session.modified = True

                if "image_feature" in request.POST:
                    request.session['image_feature'] = img.pk
                    request.session.modified = True

                messages.success(request, "Image Uploaded successfully")
                return redirect('dashboard')
            else:
                messages.error(request, "You need to upload image first")
                return redirect('dashboard')

        if 'classify' in request.POST:

            if "re_upload_class" in request.POST:
                request.session['img_class_id'] = None
                request.session['img_pred'] = None
                request.session.modified = True
                return redirect('dashboard')
            else:
                user = User.objects.get(username=request.user.username)

                img_class = Images.objects.get(id=request.POST.get('classify'))
                image_classification = classify_image("./" + img_class.img.url)

                request.session['dash_panel'] = "0"
                request.session['img_class_id'] = img_class.id
                request.session['img_pred'] = image_classification

                request.session.modified = True

                return redirect('dashboard')

        if 'image_segment' in request.POST:
            if "re_upload_segment" in request.POST:
                request.session['img_seg_id'] = None
                request.session.modified = True
                return redirect('dashboard')
            else:

                img_seg = Images.objects.get(id=int(request.POST.get('analyse')))
                image_path = "./" + img_seg.img.url

                try:
                    image_seg_result = ImageSegment.objects.get(img_id=int(request.session['img_seg_id']))
                    print(image_seg_result)
                    request.session['dash_panel'] = "1"
                    request.session['img_seg_id'] = image_seg_result.img_id.id
                    request.session.modified = True
                    messages.success(request, "Re-segmenting selected image")
                except Exception:
                    image_seg_result = ImageSegment()
                    image_seg_result.img_id = img_seg

                    img_s = segment_image(image_path, request.user.username)

                    image_seg_result.segment = img_s
                    image_seg_result.save()

                    messages.success(request, "Segmentation created!")
                    request.session['dash_panel'] = "1"
                    request.session['img_seg_id'] = img_seg.id
                    request.session.modified = True

                return redirect('dashboard')

        if "re_upload_class" in request.POST:
            request.session['img_class_id'] = None
            request.session['img_pred'] = None
            request.session.modified = True
            return redirect('dashboard')

        if "re_upload_segment" in request.POST:
            request.session['img_seg_id'] = None

            request.session.modified = True
            return redirect('dashboard')

        if 'del' in request.POST:

            image = Images.objects.get(id=int(request.POST.get('del')))

            try:
                image_segm = ImageSegment.objects.get(img_id=image)

                os.remove("./media/user_imgs_segment/" + image_segm.segment.name)
                image_segm.delete()
            except Exception:
                print("No image segments were found!")

            try:
                image_sim = ImageSimilarity.objects.get(img1=image)
                os.remove("."+image_sim.img2.url)

                try:
                    os.remove("."+image_sim.img_result.url)
                except Exception:
                    print("No Image Result file!")

                image_sim.delete()
            except ObjectDoesNotExist:
                print("No similarity row found")

            os.remove("./"+image.img.url)
            image.delete()

            request.session['img_class'] = None
            request.session['img_seg_id'] = None
            request.session['img_class_id'] = None
            request.session['img_pred'] = None
            request.session['img_id'] = None
            request.session['image_feature'] = None
            request.session.modified = True

            messages.success(request, "Image removed successfully")
            return redirect('dashboard')

        if 'upload_img_sim' in request.POST:
            print("Image similarity")
            if 0 < len(request.FILES) < 3:
                if "img1" in request.FILES and "img2" in request.FILES:
                    user = User.objects.get(username=request.user.username)

                    img1 = Images()
                    img2 = ImageSimilarity()

                    img1.user = user
                    img1.img = request.FILES['img1']

                    img2.img1 = img1

                    img2.img2 = request.FILES['img2']

                    img1.save()
                    img2.save()

                    image_path1 = "./" + img1.img.url
                    image_path2 = "./" + img2.img2.url

                    similarity_result = image_similarity(image_path1, image_path2, img1.user.username)

                    img2.img_result = similarity_result[0]
                    img2.img_similarity_score = similarity_result[1]
                    img2.save()

                    print(similarity_result)

                    request.session['img_sim'] = img1.pk
                    request.session.modified = True

                    messages.success(request, "Image Uploaded successfully")
                else:
                    messages.error(request, "Make sure both images are uploaded")

            else:
                messages.error(request, "You need to upload image first")

            return redirect('dashboard')

        if 're_upload_similarity' in request.POST:
            request.session['img_sim'] = None
            request.session.modified = True
            return redirect('dashboard')

        if 're_upload_feature' in request.POST:
            request.session['image_feature'] = None
            request.session.modified = True
            return redirect('dashboard')

        if 'extract_feature' in request.POST:
            img = Images.objects.get(pk=int(request.POST.get('extract_feature')))
            extracted_image = cv2.imread("./" + img.img.url, cv2.IMREAD_GRAYSCALE)
            # hist, bins = np.histogram(extracted_image.flatten(), bins=256, range=[0, 256])

            hist = cv2.calcHist([extracted_image], [0], None, [256], [0, 10])
            # norm = [element for row in hist for element in row]
            one_dim_array = [element for row in hist for element in row]

    return render(request, "dashboard.html", {
        "title": "Dashboard",
        "dash_panel": request.session['dash_panel'],
        "imgs": page,
        "page_no": page,
        "selected_image_segment": img_seg,
        "selected_image_segment_result": image_seg_result,
        "selected_image_classification": img_class,
        "prediction": image_classification,
        "selected_similar_image": similar_image,
        "selected_similar_image_result": similar_image_result,
        "hist": one_dim_array,
        "image_feature": image_feature
    })


def scrap_image(request):

    result = []

    if request.method == "POST":
        print(request.POST['site-name'])

        if request.POST['site-name'] == "":
            messages.error(request, "Please provide a url!")
            return redirect('scrap')

        try:
            res = get(request.POST['site-name'])

            bs = BeautifulSoup(res.text, 'html.parser')

            imgs = bs.find_all('img')

            if len(imgs) > 0:
                for img in imgs:
                    if "https" in img.get('src') or "https" in img.get('src'):
                        result.append(img.get('src'))
            else:
                messages.error(request, "Didn't find any images on this site!")
                return redirect("scrap")

            # return render(request, "scrap.html", {"title": "Scrap Image", "links": result})

            # return redirect("scrap")

        except Exception as e:
            print(e)
            messages.error(request, "Please provide a valid url!")
            return redirect("scrap")

    return render(request, "scrap.html", {"title": "Scrap Image", "links": result})

