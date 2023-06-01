from django.urls import path
from . import views


urlpatterns = [
    path("login", views.login_request,name="login"),
    path("",views.home,name="home"),
    path('register', views.register_user, name='register'),
    path('profile',views.profile,name='profile'),
    path('shop',views.shop,name='shop'),
    path("cart",views.cart,name="cart"),
    path("product/<slug:slugs>/<int:id>",views.ViewProduct,name='Product'),
    path('logout',views.logout_user,name='logout'),
    path('addtocart', views.addToCart, name='addtocart'),
    path('checkout/<int:total>',views.checkout_session,name='checkout'),
    path('success',views.success,name='success'),
    path('paymenterror',views.payError,name='payerror'),
    
]
