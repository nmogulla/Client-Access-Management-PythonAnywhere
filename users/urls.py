from django.conf.urls import url
from django.urls import path, include
# from . import views
from .views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url = '/'), name='change_password'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html", success_url = '/'), name='password_reset')
]
