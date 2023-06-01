from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    
    category_name=models.CharField(max_length=120,null=False)
    category_image=models.ImageField( upload_to="categories",null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    product_name=models.CharField(max_length=100,null=False)
    price=models.IntegerField(null=False)
    description=models.TextField(null=False)
    specification=models.CharField(max_length=200,null=False)
    slugs = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    productId=models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField( upload_to="Product_images")
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user_id = models.ForeignKey(User,  on_delete=models.CASCADE, null=False)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    product_image=models.ForeignKey(ProductImage,on_delete=models.CASCADE,null=False,default=0)
    quantity=models.IntegerField(default=1)
    created_at = models.DateTimeField(verbose_name='created date',default=timezone.now)


class NewLetter_subscribers(models.Model):
    email_id=models.EmailField(max_length=254);
    created_at = models.DateTimeField(auto_now_add=True)



