from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'crm'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('service_list', views.service_list, name='service_list'),
    path('service/create/', views.service_new, name='service_new'),
    path('service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('product_list', views.product_list, name='product_list'),
    path('product/create/', views.product_new, name='product_new'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('customer/<int:pk>/summary/', views.summary, name='summary'),
    path('signup/', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(), {'template_name': 'registration/login.html'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
