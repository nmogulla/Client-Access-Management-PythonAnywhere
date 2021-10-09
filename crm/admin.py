from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Customer, Product, Service


class CustomerList(admin.ModelAdmin):
    list_display = ('cust_name', 'organization', 'phone_number')
    list_filter = ('cust_name', 'organization')
    search_fields = ('cust_name',)
    ordering = ['cust_name']


class ServiceList(admin.ModelAdmin):
    list_display = ('cust_name', 'service_category', 'setup_time')
    list_filter = ('cust_name', 'setup_time')
    search_fields = ('cust_name',)
    ordering = ['cust_name']


class ProductList(admin.ModelAdmin):
    list_display = ('cust_name', 'product', 'pickup_time')
    list_filter = ('cust_name', 'pickup_time')
    search_fields = ('cust_name',)
    ordering = ['cust_name']


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Service)
