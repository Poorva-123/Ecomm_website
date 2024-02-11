from django.urls import path
from storeapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home',views.home),
    path('edit',views.edit),
    path('delete/<id>',views.delete),
    path('edit/<id>',views.edit),   
    path('greet',views.greet), 
    path('addproduct',views.addproduct),
    path('index',views.index),
    path('about',views.about),
    path('cart',views.viewcart),
    path('contact',views.contact),
    path('details/<id>',views.details),
    path('login',views.user_login),
    path('order',views.order),
    path('payment',views.payment),
    path('register',views.register),
    path('catfilter/<cv>',views.catfilter),
    path('pricerange',views.pricerange),
    path('sort/<sv>',views.sort),
    path('filterbyname',views.filterbyname),
    path('logout',views.user_logout),
    path('addcart/<rid>',views.addcart),
    path('remove/<id>',views.remove),
    path('qty/<sig>/<pid>',views.carqty),
    path('placeorder',views.place_order),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendmail),
    
]

if settings.DEBUG:
    urlpatterns+=static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)