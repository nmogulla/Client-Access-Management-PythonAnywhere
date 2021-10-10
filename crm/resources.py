from import_export import resources
from .models import Customer


class CustomerReport(resources.ModelResource):
    class Meta:
        model = Customer
