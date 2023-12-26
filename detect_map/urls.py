from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register, name='signup'),
    path('signin/', views.login_user, name='signin'),
    path('signout/', views.logout_user, name='signout'),
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scrap/', views.scrap_image, name='scrap')
]
