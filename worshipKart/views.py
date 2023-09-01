from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from . import models, forms
from django.contrib import messages
from django.contrib.auth import logout
from django.core import serializers
# Create your views here.


def showOrders(request):
    email = request.session['email']
    data = models.orders.objects.filter(userId__email=email)
    return render(request, 'showorders.html', {'data': data})


class respondComplaintView(View):
    def get(self, request, id):
        obj = get_object_or_404(models.complaints, complaintID=id)
        myForm = forms.adminComplaintForm(instance=obj)
        return render(request, 'complaintresolution.html', {'myForm': myForm})

    def post(self, request, id):
        obj = get_object_or_404(models.complaints, complaintID=id)
        myForm = forms.adminComplaintForm(request.POST, instance=obj)
        if myForm.is_valid():
            myForm.save()
        return redirect('collections')


def allcomplaint(request):
    email_in_session = request.session.get('email')

    if email_in_session == 'admin@worshipkart.com':
        data = models.complaints.objects.all()
        print(data)
    else:
        if email_in_session:
            user_master = get_object_or_404(
                models.userMaster, email=email_in_session)
            data = models.complaints.objects.filter(email=user_master)
        else:
            return HttpResponse("You are not logged in or have no access to complaints.")

    return render(request, 'showcomplaint.html', {'data': data})


def about(request):
    return render(request, 'aboutus.html')


class complaintView(View):
    def get(self, request):
        myForm = forms.complaintForm()
        return render(request, 'complaint.html', {'myForm': myForm})

    def post(self, request):
        # creating an instance of the compliant model
        complaint = models.complaints()
        # Since 'email' is a ForeignKey, retrieve the userMaster instance.
        # associated with the email address provided in the form.
        try:
            email = request.POST['email']
            user_master = models.userMaster.objects.get(email=email)
            complaint.email = user_master
        except:
            messages.error(
                request, 'Incorrect email, please use your registered email')
            myForm = forms.complaintForm()
            return render(request, 'complaint.html', {'myForm': myForm})
        complaint.complaintType = request.POST['complaintType']
        complaint.issue = request.POST['issue']
        complaint.save()
        return render(request, 'complaintsuccess.html')


# create order


class orderCreationView(View):
    def get(self, request):
        if request.session['myCart'] == []:
            messages.success(request, 'Cart is Empty')
            return redirect('collections')
        else:
            self.myData = []
            totalPrice = []
            netpay = []
            cart = request.session['myCart']
            for item in cart:
                productId = models.products.objects.get(
                    productId=item.get('productId'))
                qty = item.get('qty')
                a = {'productId': productId, 'qty': qty}
                self.myData.append(a)
                totalPrice.append(productId.price)
                messages.success(request, 'Order Summary')
                netpay.append((productId.price*5)/100)
            totalPrice = sum(totalPrice)
            netpay = sum(netpay)
            return render(request, 'ordersummary.html', {'myData': self.myData, 'totalPrice': totalPrice, 'netpay': netpay})


class orderConfirm(View):
    def get(self, request, tp, np):
        totalPrice = tp
        netpay = np
        myForm = forms.orderForm()
        return render(request, 'orderconfirmation.html', {'totalPrice': totalPrice, 'netpay': netpay, 'myForm': myForm})

    def post(self, request, tp, np):
        totalPrice = tp
        netpay = np
        orderPrice = eval(totalPrice)-eval(netpay)
        # print(orderPrice)
        # print('****************************************')
        cart = request.session['myCart']
        # print(cart)
        # print('****************************************')
        prolist = []
        order = models.orders()
        for item in cart:
            productId = models.products.objects.get(
                productId=item.get('productId'))
            qty = item.get('qty')
            order_product = models.OrderProduct(
                order=order, product=productId, qty=qty)
            prolist.append(order_product)
        paymentMode = request.POST.get('paymentMode')
        address = request.POST.get('address')
        text = request.session['userName']
        text1 = text.split()
        text1 = text1[0]
        userId = get_object_or_404(models.userMaster, firstName=(text1))
        order.paymentMode = paymentMode
        order.address = address
        order.userId = userId
        order.orderPrice = orderPrice
        order.save()
        for order_product in prolist:
            order_product.save()
        request.session['myCart'] = []
        request.session.modified = True
        return render(request, 'orderplaced.html')

# empty cart:


def emptycart(request):
    request.session['myCart'] = []
    request.session.modified = True
    return HttpResponse('Cart Deleted')

# Show Cart:


class showCartView(View):
    myData = []

    def get(self, request):
        if 'myCart' not in request.session or not request.session['myCart']:
            messages.success(request, 'Cart is Empty')
            return redirect('collections')
        else:
            self.myData = []
            cart = request.session['myCart']
            for item in cart:
                productId = models.products.objects.get(
                    productId=item.get('productId'))
                qty = item.get('qty')
                a = {'productId': productId, 'qty': qty}
                self.myData.append(a)
            print("=========================================================")
            print('printing myData: ', self.myData)
            print("=========================================================")
            messages.success(request, 'Products added to Cart')
            return render(request, 'cart.html', {'myData': self.myData})


def delCart(request, id, qty):
    print('del cart wala session:', (request.session['myCart']))
    for d in request.session['myCart']:
        if d.get('productId') == id and d.get('qty') == qty:
            request.session['myCart'].remove(d)
            request.session.modified = True
            messages.success(request, 'Cart Updated')
    return redirect('collections')


# add items to cart
class addtocart(View):
    # to avoid duplicates
    cart = []

    def post(self, request):
        if 'myCart' not in request.session:
            request.session['myCart'] = []
        self.cart = request.session['myCart']
        productId = request.POST['proid']
        qty = request.POST['countinput']
        a = {'productId': productId,
             'qty': qty}
        if a.get('productId') not in self.cart:
            self.cart.append(a)
            messages.success(request, 'Product added to cart')
        request.session['myCart'] = self.cart
        return redirect('collections')


class productListByCategory(View):
    def get(self, request, id):
        prolist = models.products.objects.filter(productCategory=id)
        # for p in prolist:
        #     print(p)
        return render(request, 'productlistbycat.html', {'prolist': prolist})


# collections product Category lists
def collections(request):
    mydata = models.productCategory.objects.all()
    return render(request, 'collections.html', {'mydata': mydata})


# Product Details
class productDetails(View):
    def get(self, request, id):
        obj = get_object_or_404(models.products, productId=id)
        return render(request, 'productdetails.html', {'obj': obj})


# update Product


def index(request):
    allpro = []
    obj = models.products.objects.all()
    return render(request, 'index.html', {'obj': obj})


class updatePro(View):
    def get(self, request, id):
        obj = get_object_or_404(models.products, productId=id)
        myForm = forms.productForm(instance=obj)
        return render(request, 'updatepro.html', {'myForm': myForm})

    def post(self, request, id):
        obj = get_object_or_404(models.products, productId=id)
        myForm = forms.productForm(request.POST, instance=obj)
        if myForm.is_valid():
            myForm.save()
            messages.success(request, 'Product Updated!')
        else:
            return render(request, 'somethingwrong.html')
        return redirect('showpro')

# Delete Product


class delPro(View):
    def get(self, request, id):
        obj = get_object_or_404(models.products, productId=id)
        myForm = forms.productForm(instance=obj)
        return render(request, 'delpro.html', {'myForm': myForm})

    def post(self, request, id):
        obj = get_object_or_404(models.products, productId=id)
        myForm = forms.productForm(instance=obj)
        if obj:
            obj.delete()
            messages.success(request, 'Product Deleted')
        else:
            return render(request, 'somethingwrong.html')
        return redirect('showpro')

# Add Product


class addPro(View):
    def get(self, request):
        myForm = forms.productForm()
        return render(request, 'addpro.html', {'myForm': myForm})

    def post(self, request):
        myForm = forms.productForm(request.POST)
        if myForm.is_valid():
            myForm.save()
        else:
            return render(request, 'somethingwrong.html')
        return redirect('showpro')

# show products list:


def showPro(request):
    obj = models.products.objects.all()
    return render(request, 'showpro.html', {'obj': obj})

# Update product Category


class updateProductCategories(View):
    def get(self, request, id):
        obj = get_object_or_404(models.productCategory, productCategoryId=id)
        print(obj)
        myForm = forms.productCategoryForm(instance=obj)
        return render(request, 'updatepc.html', {'myForm': myForm})

    def post(self, request, id):
        obj = get_object_or_404(models.productCategory, productCategoryId=id)
        myForm = forms.productCategoryForm(request.POST, instance=obj)
        if myForm.is_valid():
            myForm.save()
            messages.success(request, 'Category Updated!')
        else:
            return render(request, 'somethingwrong.html')
        return redirect('showpc')

# Delete product Category


class delProductCategory(View):
    def get(self, request, id):
        obj = get_object_or_404(models.productCategory, productCategoryId=id)
        myForm = forms.productCategoryForm(instance=obj)
        print(obj)
        return render(request, 'delpc.html', {'myForm': myForm})

    def post(self, request, id):
        obj = get_object_or_404(models.productCategory, productCategoryId=id)
        obj.delete()
        messages.success(request, 'Selected Product Category is deleted')
        return redirect('showpc')


def showProductCategories(request):
    myData = models.productCategory.objects.all()
    return render(request, 'showproductcategory.html', {'myData': myData})


class productCategoryView(View):
    def get(self, request):
        myform = forms.productCategoryForm()
        return render(request, 'addproductcategory.html', {'myform': myform})

    def post(self, request):
        myform = forms.productCategoryForm(request.POST)
        if myform.is_valid():
            myform.save()
            messages.success(request, 'Category added successfully')
            return redirect('addpc')
        else:
            return render(request, 'somethingwrong.html')

# Login/Logout Views:->


class SigninView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        password1 = request.POST['password1']
        email = request.POST['email']
        userData = models.userMaster.objects.filter(
            email__exact=email).filter(password__exact=password1)
        if userData:
            for dt in userData:
                request.session['userName'] = dt.firstName + " "+dt.lastName
                request.session['userType'] = dt.userType
                request.session['email'] = dt.email
            # return render(request, 'collections.html', {'userData': userData})
            return redirect('collections')
        else:
            messages.error(request, 'Invalid credentials. Please try again')
            return redirect('signin')


def signOut(request):
    print('user name is ', request.session['userName'])
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('signin')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ct = request.POST['phone']
        em = request.POST['email']
        ps = request.POST['password1']
        print(request.POST.get('chk'))

        if 'chk' in request.POST:
            nl = request.POST.get('chk')
        else:
            nl = False
        print("values are = ", fn, ln, ct, em, ps, nl)
        obj = models.userMaster.objects.create(
            firstName=fn, lastName=ln, contact=ct, email=em, password=ps, newsletter=nl)
        obj.save()
        return redirect('signin')


def home(request):
    return render(request, 'base.html')


def incense(request):
    prolist = models.products.objects.filter(productCategory='pc400')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def dhoop(request):
    prolist = models.products.objects.filter(productCategory='pc500')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def wicks(request):
    prolist = models.products.objects.filter(productCategory='pc600')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def gangajal(request):
    prolist = models.products.objects.filter(productCategory='pc700')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def matchbox(request):
    prolist = models.products.objects.filter(productCategory='pc800')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def kapoor(request):
    prolist = models.products.objects.filter(productCategory='pc900')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def kapoor(request):
    prolist = models.products.objects.filter(productCategory='pc900')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def crystal(request):
    prolist = models.products.objects.filter(productCategory='pc100')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def bracelet(request):
    prolist = models.products.objects.filter(productCategory='pc1000')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def fumers(request):
    prolist = models.products.objects.filter(productCategory='pc200')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def fengshui(request):
    prolist = models.products.objects.filter(productCategory='pc1100')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def vastu(request):
    prolist = models.products.objects.filter(productCategory='pc1200')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def yantra(request):
    prolist = models.products.objects.filter(productCategory='pc1300')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def thali(request):
    prolist = models.products.objects.filter(productCategory='pc1400')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def aura(request):
    prolist = models.products.objects.filter(productCategory='pc1500')
    return render(request, 'productlistbycat.html', {'prolist': prolist})


def roomdecor(request):
    prolist = models.products.objects.filter(productCategory='pc1600')
    return render(request, 'productlistbycat.html', {'prolist': prolist})
