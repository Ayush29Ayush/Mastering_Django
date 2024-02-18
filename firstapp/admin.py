from django.contrib import admin

from firstapp.models import Product, Cart, ProductInCart, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(Order)
