from django.db import models
import datetime

# Create your models here.


class userMaster(models.Model):
    uc = [('Buyer', 'Buyer'), ('Admin', 'Admin')]
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    contact = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    newsletter = models.BooleanField()
    userType = models.CharField(max_length=10, choices=uc, default='Buyer')

    def __str__(self):
        return self.firstName+" - "+self.lastName+" - "+self.email+" - "+self.userType


class productCategory(models.Model):
    productCategoryId = models.CharField(max_length=30, primary_key=True)
    productCategoryName = models.CharField(max_length=100)
    categoryImages = models.ImageField(
        upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.productCategoryName


class products(models.Model):
    productId = models.CharField(primary_key=True, max_length=30)
    productName = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    description = models.TextField()
    productimage = models.ImageField(upload_to='images', null=True, blank=True)
    productCategory = models.ForeignKey(
        productCategory, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.productName+" - "+self.productId


class quantity(models.Model):
    qty = models.IntegerField()
    product = models.ForeignKey(products, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.qty)+self.product


class orders(models.Model):
    orderId = models.AutoField(primary_key=True)
    products = models.ManyToManyField(products, through='OrderProduct')
    userId = models.ForeignKey(userMaster, on_delete=models.CASCADE)
    orderDate = models.DateField(default=datetime.date.today)
    transactionMode = [('IB', 'Internet Banking'), ('Wallet',
                                                    'Wallet'), ('UPI', 'UPI'), ('COD', 'Cash on Delivery')]
    orderPrice = models.DecimalField(decimal_places=2, max_digits=15)
    paymentMode = models.CharField(max_length=100, choices=transactionMode)
    address = models.TextField(blank=False, null=False)

    def __str__(self):
        return str(self.orderId)+" - "+str(self.orderDate)


class OrderProduct(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return str(self.order)


class complaints(models.Model):
    ct = [('Product Related', 'Product Related'), ('Delivery related', 'Delivery related'),
          ('Payment Related', 'Payment Related'), ('Others', 'Others')]

    st = [('Open', 'Open'), ('Awaiting Customer Response', 'Awaiting Customer Response'), ('Under Review', 'Under Review'), ('Resolved',
                                                                                                                             'Resolved'), ('Awaiting Vendor Response', 'Awaiting Vendor Response')]
    complaintID = models.AutoField(primary_key=True)
    complaintDate = models.DateField(default=datetime.date.today)
    complaintType = models.CharField(
        choices=ct, default='Others', max_length=100)
    complaintStatus = models.CharField(
        choices=st, default='Open', max_length=100)
    email = models.ForeignKey(userMaster, on_delete=models.CASCADE)
    issue = models.TextField()
    response = models.TextField(blank=True, null=True)
    responseDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.complaintID)+" - "+str(self.email)
