import datetime
import tempfile

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from _decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.template.loader import render_to_string
from import_export.formats.base_formats import HTML
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A3
import io
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import csv
from tablib import Dataset
from .resources import CustomerReport
from django.core.files.storage import FileSystemStorage

from .forms import *
from .models import *

now = timezone.now()


def home(request):
    return render(request, 'crm/home.html',
                  {'crm': home})


@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html',
                  {'customers': customer})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'crm/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('crm:customer_list')


# Service List
@login_required
def service_list(request):
    services = Service.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/service_list.html', {'services': services})


# Service new
@login_required
def service_new(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html',
                          {'services': services})
    else:
        form = ServiceForm()
        # print("Else")
    return render(request, 'crm/service_new.html', {'form': form})


# Service Edit
@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            # service.customer = service.id
            service.updated_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services': services})
    else:
        # print("else")
        form = ServiceForm(instance=service)
    return render(request, 'crm/service_edit.html', {'form': form})


# Service Delete

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('crm:service_list')


@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = \
        Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = \
        Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))

    # if no product or service records exist for the customer,
    # change the ‘None’ returned by the query to 0.00
    sum = sum_product_charge.get("charge__sum")
    if sum is None:
        sum_product_charge = {'charge__sum': Decimal('0')}
    sum = sum_service_charge.get("service_charge__sum")
    if sum is None:
        sum_service_charge = {'service_charge__sum': Decimal('0')}

    return render(request, 'crm/summary.html', {'customer': customer,
                                                'products': products,
                                                'services': services,
                                                'sum_service_charge': sum_service_charge,
                                                'sum_product_charge': sum_product_charge, })


# Product views
@login_required
def product_list(request):
    products = Product.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/product_list.html', {'products': products})


# product new
@login_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html',
                          {'products': products})
    else:
        form = ProductForm()
        # print("Else")
    return render(request, 'crm/product_new.html', {'form': form})


# Product Edit
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': products})
    else:
        # print("else")
        form = ProductForm(instance=product)
    return render(request, 'crm/product_edit.html', {'form': form})


# Product Delete

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('crm:product_list')


# SignUp form

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'crm/home.html',
                          {'crm': home})
    else:
        form = UserCreationForm()
    return render(request, 'crm/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    request.session.flush()
    return render(request, 'crm/home.html',
                  {'crm': home})


def export_csv(request):
    # if request.method == 'POST':
    # Get selected option from form
    # file_format = request.POST['file-format']
    customer_report = CustomerReport()
    dataset = customer_report.export()
    # if file_format == 'CSV':
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=exported_data.csv'
    return response


def export_pdf(request):
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    x = Customer.objects.all()
    p = canvas.Canvas(buffer, pagesize=A3, bottomup=0)
    textobj = p.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)
    for a in x:
        textobj.textLine('Customer Name: '+ a.cust_name)
        textobj.textLine('Organization: ' + a.organization)
        textobj.textLine('Role: ' + a.role)
        textobj.textLine('Email: ' + a.email)
        textobj.textLine('Phone Number: ' + a.phone_number)
        textobj.textLine('Building Room: ' + a.bldgroom)
        textobj.textLine('Account Number: ' + str(a.account_number))
        textobj.textLine('Address: ' + a.address)
        textobj.textLine('City: ' + a.city)
        textobj.textLine('State: ' + a.state)
        textobj.textLine('Zip Code: ' + a.zipcode)
        textobj.textLine()

    p.drawText(textobj)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='exported_pdf' + str(datetime.datetime.now()) + '.pdf')
