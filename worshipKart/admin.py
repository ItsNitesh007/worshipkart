from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.userMaster)
admin.site.register(models.productCategory)
admin.site.register(models.products)
admin.site.register(models.orders)
admin.site.register(models.OrderProduct)
admin.site.register(models.quantity)
admin.site.register(models.complaints)
