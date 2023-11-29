from django.urls import path, include
# import SaltToTasteProject.SaltToTasteProject.settings
# from django.conf import settings
from SaltToTasteProject import settings
from .views import *
from django.contrib.auth.views import LogoutView
# from .views import views

urlpatterns = [
    # path('', views.index, name='home'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    # path('sign/')
    # path('profile/', views.profile, name='profile'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # path('toggle_subscription/<int:user_id>/', toggle_subscription, name='toggle_subscription'),
]
