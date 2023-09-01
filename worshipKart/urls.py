from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # user management
    path('signin', views.SigninView.as_view(), name='signin'),
    path('signout', views.signOut, name='signout'),
    path('register', views.RegisterView.as_view(), name='register'),
    # Product Category
    path('addpc', views.productCategoryView.as_view(), name='addpc'),
    path('showpc', views.showProductCategories, name='showpc'),
    path('updatepc/<id>', views.updateProductCategories.as_view(), name='updatepc'),
    path('delpc/<id>', views.delProductCategory.as_view(), name='delpc'),
    # product
    path('addpro', views.addPro.as_view(), name='addpro'),
    path('showpro', views.showPro, name='showpro'),
    path('updatepro/<id>', views.updatePro.as_view(), name='updatepro'),
    path('delpro/<id>', views.delPro.as_view(), name='delpro'),
    path('index', views.index, name='index'),
    path('productdetails/<id>', views.productDetails.as_view(),
         name='productdetails'),
    # homepage
    path('', views.collections, name='collections'),
    path('collections', views.collections, name='collections'),
    path('prolistbycat/<id>', views.productListByCategory.as_view(),
         name='prolistbycat'),
    path('addtocart', views.addtocart.as_view(), name='addtocart'),
    path('cart', views.showCartView.as_view(), name='cart'),
    path('emptycart', views.emptycart, name='emptycart'),
    path('delcart/<id>/<qty>', views.delCart, name='delcart'),
    path('ordersummary', views.orderCreationView.as_view(), name='ordersummary'),
    path('orderconfirm/<tp>/<np>',
         views.orderConfirm.as_view(), name='orderconfirm'),
    path('showorders', views.showOrders, name='showorders'),
    # complaint and about us
    path('about', views.about, name='about'),
    path('complaint', views.complaintView.as_view(), name='complaint'),
    path('allcomplaint', views.allcomplaint, name='allcomplaint'),
    path('respondcomplaint/<id>', views.respondComplaintView.as_view(),
         name='respondcomplaint'),
    # navbar
    path('incense', views.incense, name='incense'),
    path('dhoop', views.dhoop, name='dhoop'),
    path('wicks', views.wicks, name='wicks'),
    path('gangajal', views.gangajal, name='gangajal'),
    path('matchbox', views.matchbox, name='matchbox'),
    path('kapoor', views.kapoor, name='kapoor'),
    path('crystal', views.crystal, name='crystal'),
    path('bracelet', views.bracelet, name='bracelet'),
    path('fumers', views.fumers, name='fumers'),
    path('vastu', views.vastu, name='vastu'),
    path('yantra', views.yantra, name='yantra'),
    path('fengshui', views.fengshui, name='fengshui'),
    path('thali', views.thali, name='thali'),
    path('aura', views.aura, name='aura'),
    path('roomdecor', views.roomdecor, name='roomdecor'),

]
