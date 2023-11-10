from django.urls import path, include
# import SaltToTasteProject.SaltToTasteProject.settings
from .views import SignUpView, Login
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),

]
