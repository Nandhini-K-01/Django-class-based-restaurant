from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view(), name='signup'),
    path('signin', views.SigninView.as_view(), name='signin'),
    path('signout', views.LogoutView.as_view(), name='signout'),
]