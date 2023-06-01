from django.contrib import admin
from ECommerceApp.models import *
# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'slugs',
                    'description', 'specification', 'created_at')
    prepopulated_fields = {'slugs': ('product_name',)}

class categoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'category_image' ,'created_at')


class NewLetter_subscribersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_id' ,'created_at')

class cartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'product_image', 'created_at')


class ProductImageAdmin(admin.ModelAdmin):
    list_display=('id','productId','image')


admin.site.register(Product,productAdmin)
admin.site.register(Category,categoryAdmin)
admin.site.register(Cart,cartAdmin)
admin.site.register(NewLetter_subscribers,NewLetter_subscribersAdmin)
admin.site.register(ProductImage,ProductImageAdmin)