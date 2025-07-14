from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy


from .views import register, email_verification, login_user, logout_user, dashboard_user, profile_user, delete_user

app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('email-verification/', email_verification, name='email-verification'),

    path('login/', login_user, name='login-user'),
    path('logout/', logout_user, name='logout-user'),

    path('dashboard/', dashboard_user, name='dashboard'),
    path('profile-user/', profile_user, name='profile-user'),
    path('delete-user/', delete_user, name='delete-user'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password-reset.html',
        email_template_name='account/password/password-reset-email.html',
        success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password-reset-done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password-reset-confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password-reset-complete.html'),
         name='password_reset_complete'),

]

