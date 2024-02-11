from django.shortcuts import render,HttpResponse,redirect
from storeapp.models import Product,Cart,Orders
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.

def home(request):
    p=Product.objects.all()
    print(p)
    context={}
    context['user']="itvedant"
    context['x']=300
    context['y']=40
    context['l']=[1,2,3,4,5]
    context['d']={'id':1,'name':'machine','price':200,'qty':50}
    context['data']=[
        {'id':1,'name':'machine','price':200,'qty':50},
        {'id':2,'name':'sunny','price':20,'qty':5},
        {'id':3,'name':'jeans','price':100,'qty':2}
    ]
    context['products']=p
    return render(request,'home.html',context)


def delete(request,id):
    p=Product.objects.filter(id=id).delete()
    print(p)
    return redirect('/home')

def edit(request,id):

    p=Product.objects.filter(id=id) # fetching a specific record, sql= select * from storeapp_product where id=id
    if(request.method=='GET'):
        context={}
        context['data']=p
        return render(request,'editproduct.html',context)
    else:
        uname=request.POST['pname']
        uprice=request.POST['price']
        uqty=request.POST['qty']
        # print(uname,uprice,uqty)
        # return HttpResponse('updated')
        p.update(name=uname,price=uprice,qty=uqty)
        return redirect('/home')
def greet(request):
    return render(request,'base.html')

def addproduct(request):
    print(request.method)
    if request.method=="GET":
        return render(request,'addproduct.html')
    else:
        print("in else part")
        product_name=request.POST['pname']
        price=request.POST['price']
        q=request.POST['qty']

        '''
        print(product_name)
        print(price)
        print(q)
        print(request)
        '''

        p=Product.objects.create(name=product_name,price=price,qty=q)
        print(p)
        p.save()

        return redirect('/home')

def about(request):
    return render(request,'about.html')

def index(request):
    uid=request.user.id
    print(uid)
    print(request.user.is_authenticated)
    p=Product.objects.filter(is_active=True)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

# def cart(request):
#     return render(request,'cart.html')

def contact(request):
    return render(request,'contact.html')

def details(request,id):
    p=Product.objects.filter(id=id)
    print(p)
    context={}
    context['products']=p
    return render(request,'details.html',context)
    

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        context={}
        user=request.POST['username']
        p=request.POST['p']
        # print(user,p)
        u=authenticate(username=user,password=p)
        # print(u)
        if u is not None:
            login(request,u)
            return redirect('/index')
        else:
            context['errmsg']="Invalid Email or Password!!!"
            return render(request,'login.html',context)

def order(request):
    return render(request,'order.html')

def payment(request):
    return render(request,'payment.html')

def placeorder(request):
    return render(request,'placeorder.html')

def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    else:
        context={}
        user=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        # print(user,p,cp)
        if user=="" or p=="" or cp=="":
            context['errmsg']="Fields cannot be empty!!!"
            return render(request,'register.html',context) 
        elif p!=cp:
            context['errmsg']="Password doesnt match"
            return render(request,'register.html',context) 
        else:
            try:
                u=User.objects.create(username=user)
                u.set_password(p)
                u.save()
                context['success']="Successfuly created"
                return render(request,'register.html',context)
            except Exception:
                context["errmsg"]="User already exist."
                return render(request,'register.html',context)



def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=1)
    #p=Product.objects.filter(cat=cv)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def pricerange(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte = min)
    q2=Q(price__lte = max)
    q3=Q(is_active=1)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p

    print(min,max)
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '1':
        para='-price'
    else:
        para='price'
    p=Product.objects.order_by(para).filter(is_active=1)

    context={}
    context['products']=p
    return render(request,'index.html',context)


def filterbyname(request):
    byname=request.GET['filtername']
    p=Product.objects.filter(name=byname)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def user_logout(request):
    logout(request)
    return redirect('/index')

def addcart(request,rid):
    context={}
    p=Product.objects.filter(id=rid)
    u=User.objects.filter(id=request.user.id)
    if request.user.is_authenticated:
        q1=Q(pid=p[0])
        q2=Q(uid=u[0])
        res=Cart.objects.filter(q1 & q2)
        if res:
            context['dup']="product already exists in Cart!!"
            context['products']=p
            return render(request,'details.html',context)
        else:
            
            print(p,u)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['products']=p
            context['success']="Product added Successfully in Cart"
            return render(request,'details.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(uid=request.user.id)
        s=0
        for x in c:
            print(x)
            print(x.qty)
            print(x.pid.price)
            s=s+(x.qty*x.pid.price)
        context['total']=s
        context['product']=c
        context['items']=len(c)
        return render(request,'cart.html',context)
    else:
        return redirect('/login')


def remove(request,id):
    c=Cart.objects.get(id=id).delete()
    return redirect('/cart')


def carqty(request,sig,pid):
    q1=Q(uid=request.user.id)
    q2=Q(pid=pid)
    c=Cart.objects.filter(q1 & q2)
    print(c)
    qty=c[0].qty
    if sig=='0':
        if qty>1:
            qty=qty-1
            c.update(qty=qty)
    else:
        qty=qty+1
        c.update(qty=qty)
    print(qty)
    return redirect("/cart")


def place_order(request):
    if User.is_authenticated:
        c=Cart.objects.filter(uid=request.user.id)
        oid=random.randrange(1000,9999)
        context={}
        s=0
        for x in c:
            o=Orders.objects.create(order_id=oid,uid=x.uid,pid=x.pid,qty=x.qty)
            o.save()
            x.delete()
        o=Orders.objects.filter(uid=request.user.id)
        i=len(o)
        for y in o:
            s=s+(y.qty*y.pid.price)
        context['product']=Orders.objects.filter(uid=request.user.id)
        context['total']=s
        context['items']=i
        return render(request,'placeorder.html',context)
    else:
        return redirect('/login')


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_Ql9tB4wL1aiwUh", "XoeVIEv9Hzs5cMFJgva8bAZh"))
    print(client)
    o=Orders.objects.filter(uid=request.user.id)
    oid=str(o[0].order_id)
    s=0
    for y in o:
        s=s+(y.qty*y.pid.price)

    s=s*100
    data = { "amount": s, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print("order id",oid)
    print("total",s)
    print(payment)
    context={}
    context['payment']=payment
    return render(request,'pay.html',context)


def sendmail(request):
    pid=request.GET['p1']
    oid=request.GET['p2']
    sign=request.GET['p3']
    rec_email=request.user.email
    msg="Your Order has been placed Successfully. Your Order Tracking ID : "+oid
    send_mail(
    "ProdctOrder Status",
    msg,
    "poorvavishwakarma115.model@gmail.com",
    [rec_email],
    fail_silently=False,
    )

    print(pid,oid,sign)
    print('mailed')
    return HttpResponse("mailed")

