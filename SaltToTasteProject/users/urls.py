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
    # path('subscribers/', subscribers, name='subscribers'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', profile_edit, name='profile_edit'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # path('get_user_recipes/', get_user_recipes, name='get_user_recipes'),
    # path('get_user_collections/', get_user_collections, name='get_user_collections'),
    path('profile/<int:pk>/subs/', subscribers, name='subs'),
    path('subscription/<int:user_id>/', subscription, name='subscription'),
    # path('toggle_subscription/<int:user_id>/', toggle_subscription, name='toggle_subscription'),
]
