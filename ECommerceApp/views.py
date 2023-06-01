import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
import stripe
from django.core.mail import send_mail
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from ECommerceApp.models import Product, ProductImage, Cart, Category, NewLetter_subscribers
from django.conf import settings
from django.urls import reverse


import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY
# Create your views here.
def login_request(request):
    if request.method=='POST':
        uname=request.POST['email']
        upass=request.POST['password']
        isUserValid=authenticate(username=uname,password=upass)
        if isUserValid is not None:
            login(request,isUserValid)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Username or Password!')
    return render(request,'frontend/login.html')


@login_required
def logout_user(request):
    if User.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return redirect('home')


def home(request):
    n=8
    images = getImageN(n)
    frontData=getImageN(3)
    activeData=getImageN(1)
    data={
        'items':frontData,
        'img':images,
        'ac':activeData
    }

    if request.method == 'POST':
        productId = request.POST['productId']
        imageid=request.POST['productImage']
        img=ProductImage.objects.get(id=imageid)
        pid=Product.objects.get(id=productId)
        res = addToCart(request,pid,img)

        if res == 1:
            messages.success(request, 'Item added to Cart')
        elif res==0:
            messages.error(request, "Item is already in cart")
    
    return render(request,'frontend/home.html',data)


def register_user(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been created. You can log in now!')
            return redirect('login')
        else:
            messages.error(
                request, 'Error!')
    else:
        form = UserRegistrationForm()
    context = {'form': form}

    return render(request, 'frontend/register.html', context)

def profile(request):
    return redirect('home')


def shop(request):
    stocks = getproducts()
    images = getImages()
    
    

    if request.method=='POST':
        if 'sortItems' in request.POST: 
            # minPrice=request.POST['min_price']
            # maxPrice=request.POST['max_price']
            sortItems=int(request.POST['sortItems'])
            
            images=sortedData(sortItems)
            print(images)

        elif 'productID' in request.POST:
            productId = request.POST['productId']
            imageid = request.POST['productImage']
            img = ProductImage.objects.get(id=imageid)
            pid = Product.objects.get(id=productId)
            res = addToCart(request, pid, img)

            if res == 1:
                messages.success(request, 'Item added to Cart')
            elif res == 0:
                messages.error(request, "Item is already in cart")

    data = {
        'prod': stocks,
        'img': images
    }

    return render(request,'frontend/shop.html',data)


def sortedData(sortItems):
    
    if sortItems == 1:
        filteredData = ProductImage.objects.all().order_by('-created_at')
    elif sortItems== 2:
        filteredData = ProductImage.objects.all().order_by('created_at')
    elif sortItems==3:
        filteredData = ProductImage.objects.all().order_by('productId__price')
    elif sortItems==4:
        filteredData = ProductImage.objects.all().order_by('-productId__price')
    
    return filteredData


def cart(request):
    items=getCartItems(request)
    total=0
    count=0
    for i in items:
        total+=i.product_id.price
        count+=1
    

    # stripe.api_key = settings.STRIPE_PRIVATE_KEY

    # session = stripe.checkout.Session.create(
    #     payment_method_types=['card'],
    #     line_items=[
    #         {
    #             "price_data": {
    #                 "currency": "usd",
    #                 "product_data": {"name": "T-shirt"},
    #                 "unit_amount": total,
    #             },
    #             "quantity": count,
    #         },
    #     ],
    #     mode='payment',
    #     success_url=request.build_absolute_uri(
    #         reverse('cart')) + '?session_id={CHECKOUT_SESSION_ID}',
    #     cancel_url=request.build_absolute_uri(reverse('home')),
    # )
    data = {
        'items': items,
        'total': total,
        'itemCount': count,
    }
    return render(request,'frontend/cart.html',data)

def ViewProduct(request,slugs,id):
    pid=id
    otherProducts=ProductImage.objects.all().exclude(productId=pid)[:4]
    products=ProductImage.objects.get(productId=pid)
    data={
        'data':products,
        'more':otherProducts
    }
    return render(request,'frontend/product_page.html',data)


def getproducts():
    allProduct=Product.objects.all()
    return allProduct

def getCartItems(request):
    if User.is_authenticated:
        uid=getUserID(request)
        items=Cart.objects.filter(user_id=uid.id)    
        return items
    

def getUserID(request):
    if User.is_authenticated:
        uid=request.user
        return uid


def getImages():
    img=ProductImage.objects.all().order_by('-created_at')
    return img


def getImageN(n):
    img = ProductImage.objects.all()[:n]
    return img


def addToCart(request,pid,img):
    if User.is_authenticated:
        uid = getUserID(request)
        check=Cart.objects.filter(user_id=uid).filter(product_id=pid).count()
        if check ==0:
            add_cart = Cart(user_id=uid, product_id=pid, product_image=img)
            add_cart.save()
            return 1
        else:
            
            return 0
    else:
        return 2



def checkout_session(request,total):
    stripe.api_key=settings.STRIPE_PRIVATE_KEY
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'npr',
                'product_data': {
                    'name': 'Cart Items',
                },
                'unit_amount': total*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/paymenterror',
    )

    return redirect(session.url,code=303)


def success(request):
    uid=getUserID(request)
    delCartItems=Cart.objects.filter(user_id=uid)
    delCartItems.delete()
    return render(request,'frontend/successfulpayment.html')

def payError(request):
    return render(request,'frontend/error.html')
