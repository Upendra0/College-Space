from os import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html', redirect_authenticated_user=True, authentication_form=UserLoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('password_change', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'), name='password_change'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),
    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile', views.profile, name='profile'),
    path('verify_account', views.verify_account, name='verify_account'),
]
