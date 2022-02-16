from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.backends import sqlite3
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import ListView, DetailView
from .models import models, Comment, Vehicle
from .models import Client
from django.urls import reverse_lazy


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'

    def get_queryset(self):
        return Client.objects.filter(author=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client_detail.html'
    login_url = 'login'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    template_name = 'client_edit.html'


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'client_new.html'
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ('comment',)
    template_name = 'comment_edit.html'


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('client_list')


# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     template_name = 'comment_create.html'
#     fields = ('comment', 'client')
#     login_url = 'login'
#
#     def form_valid(self, form, request):
#         form.instance.author = self.request.user
#         # Comment.objects.filter('form.instance.client_id = self.request.user.id').first()
#         #form.instance.client_id = self.request.user
#         return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_create.html'
    fields = ('comment', 'client')
    login_url = 'login'

    def get_queryset(self):
        return Client.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Comment.objects.filter('form.instance.client_id = self.request.user.id').first()
        form.instance.Client = Client.objects.filter(author=self.request.user)
        return super().form_valid(form)


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    template_name = 'vehicle_create.html'
    fields = ('make', 'model', 'VIN_number', 'date_of_purchase', 'date_of_last_service', 'client')
    login_url = 'login'
    success_url = reverse_lazy('client_list')

    def get_queryset(self):
        return Client.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Comment.objects.filter('form.instance.client_id = self.request.user.id').first()
        form.instance.Client = Client.objects.filter(author=self.request.user)
        return super().form_valid(form)


class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicle_delete.html'
    success_url = reverse_lazy('client_list')


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    fields = ('make', 'model', 'VIN_number', 'date_of_purchase', 'date_of_last_service',)
    template_name = 'vehicle_edit.html'
    success_url = reverse_lazy('client_list')
