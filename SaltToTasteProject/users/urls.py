from django.urls import path, include

from SaltToTasteProject import settings
from users.views import SignUpView, LoginUser
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('registration/', SignUpView.as_view(), name='registrations'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')

]
