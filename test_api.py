import requests


url_register = "http://127.0.0.1:8000/register/"
url_image_c = "http://127.0.0.1:8000/image-classify/"
url_image_s = "http://127.0.0.1:8000/image-segment/"
url_login = "http://127.0.0.1:8000/login/"
url_logout = "http://127.0.0.1:8000/logout/"

files = {'media': open('Forest_1.jpg', 'rb')}

res = requests.post(url_image_c, data={"msg": "Forest Image"}, files=files)

print(res.json())

