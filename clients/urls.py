from django.urls import path
from . import views
from .views import (
    ClientListView,
    ClientUpdateView,
    ClientDetailView,
    ClientDeleteView,
    ClientCreateView,
    CommentUpdateView,
    CommentDeleteView,
    CommentCreateView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
)

urlpatterns = [

    path('<int:pk>/edit/',
         ClientUpdateView.as_view(), name='client_edit'),
    path('<int:pk>/',
         ClientDetailView.as_view(), name='client_detail'),
    path('<int:pk>/delete/',
         ClientDeleteView.as_view(), name='client_delete'),
    path('', ClientListView.as_view(), name='client_list'),
    path('new/', ClientCreateView.as_view(), name='client_new'),
    path('<int:pk>/commentedit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('<int:pk>/commentdelete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('commentcreate/', CommentCreateView.as_view(), name='comment_create'),
    path('vehiclecreate/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('<int:pk>/vehicleedit/', VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('<int:pk>/vehicledelete/', VehicleDeleteView.as_view(), name='vehicle_delete'),
   # path('commentcreate/', CommentCreateView.as_view(), name='comment_create'),

]
