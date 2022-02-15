from django.contrib import admin

# Register your models here.
from .models import Client, Comment, Vehicle


class CommentInline(admin.TabularInline):
    model = Comment


class VehicleInfo(admin.TabularInline):
    model = Vehicle


class ClientAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        VehicleInfo,
    ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Comment)
admin.site.register(Vehicle)

