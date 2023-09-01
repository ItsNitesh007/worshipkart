from django import forms
from . import models


class productCategoryForm(forms.ModelForm):

    class Meta:
        model = models.productCategory
        fields = "__all__"
        labels = {
            'productCategoryId': 'Category ID',
            'productCategoryName': 'Category Name',
        }


class productForm(forms.ModelForm):

    class Meta:
        model = models.products
        fields = "__all__"


class orderForm(forms.ModelForm):
    class Meta:
        model = models.orders
        fields = ["address", "paymentMode",]
        labels = {
            'address': 'Address',
            'paymentMode': 'Payment Method'
        }


class complaintForm(forms.ModelForm):
    # CharField for email
    email = forms.CharField(max_length=100, label='Registered Email')

    class Meta:
        model = models.complaints
        fields = ['complaintType', 'email', 'issue',]
        labels = {
            'complaintType': 'Query/Complaint related to',
            'email': 'Registered Email',
            'issue': 'Please elaborate the issue'
        }


class adminComplaintForm(forms.ModelForm):
    class Meta:
        model = models.complaints
        exclude = ["email"]
        labels = {
            'complaintID': 'ID',
            'complaintStatus': 'Status',
            'complaintType': 'Query/Complaint related to',
            'issue': 'Please elaborate the issue',
            'response': 'Response',
            'responseDate': 'Response Date (YYYY-MM-DD)'
        }
