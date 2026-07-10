from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from .forms import StyledPasswordResetForm, StyledSetPasswordForm

app_name = 'users'

urlpatterns = [
    path('register/',                    views.register_view,      name='register'),
    path('login/',                       views.login_view,         name='login'),
    path('logout/',                      views.logout_view,        name='logout'),
    path('profile/',                     views.profile_view,       name='profile'),
    path('profile/edit/',                views.edit_profile_view,  name='edit_profile'),
    path('address/add/',                 views.add_address_view,   name='add_address'),
    path('address/<int:pk>/delete/',     views.delete_address_view,name='delete_address'),

    # ── Forgot password ──────────────────────────────────────────
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt',
             form_class=StyledPasswordResetForm,
             extra_email_context={'site_name': settings.SITE_NAME},
             success_url='/users/password-reset/done/',
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             form_class=StyledSetPasswordForm,
             success_url='/users/password-reset/complete/',
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
