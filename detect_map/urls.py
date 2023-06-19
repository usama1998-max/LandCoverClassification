from django.urls import path
from . import views
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Rest Framework URLs
    path('home/', TemplateView.as_view(template_name="index.html"), name="home"),
    path('signup/', TemplateView.as_view(template_name="index.html")),
    path('signin/', TemplateView.as_view(template_name="index.html")),

    # JWT token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # React URLs
    path('image-classify/', views.image_classify, name='image-classify'),
    path('image-segment/', views.image_segment, name='image-segment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
