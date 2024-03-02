from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    
    #! Here we created a custom function to update the price of a product
    @classmethod
    def updateprice(cls, product_id, price):
        product = cls.objects.filter(product_id=product_id)
        product = product.first()
        product.price = price
        product.save()
        return product
    
    #! Here we created a custom function to create a product. We can now use Product.create(product_name=product_name, price=price) rather than using Product.objects.create(product_name=product_name, price=price)
    @classmethod
    def create(cls, product_name, price):
        product = cls(product_name=product_name, price=price)
        product.save()
        return product
    #! Its better to use classmethod rather than using staticmethod for creating such custom functions

    def __str__(self):
        return self.product_name



#! This is a model manager. We can use this to create a cart for a user. We can also perform any other actions we want to perform.
class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        # you can perform any other actions you want to perform
        return cart
    
    
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    
    #! Since we want to use our custom manager, we are defining objects = CartManager(), otherwise by default, it will use its default django manager. This is the objects in the Cart.objects.create() command, which we want to override so we are using create_cart rather than the default create. Now the command will be Cart.objects.create_cart() rather than Cart.objects.create()
    objects = CartManager()
    
    #! Custom manager with a different name
    # Now, you would use Cart.custom_manager.create_cart() instead of Cart.objects.create_cart() to create a new cart instance using the custom manager method.
    custom_manager = CartManager()


class ProductInCart(models.Model):
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "product")


class Order(models.Model):
    status_choices = (
        (1, "Not Packed"),
        (2, "Ready for Shipment"),
        (3, "Shipped"),
        (4, "Delivered"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices, default=1)
