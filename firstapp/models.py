from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, AbstractBaseUser

# from django.utils.translation import ugettext_lazy as _ #! ugettext_lazy got deprecated
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

from django.contrib.auth.models import PermissionsMixin

# Create your models here.

#! Here we are inheriting the default User Model by inheriting the AbstractUser. An abstract base class implements a fully featured User model with admin-compliant permissions. Username and password are required. Other fields are optional. AbstractUser equals to the User Model provided by django by default with all the necessary fields
# class  CustomUser(AbstractUser):
# class  CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(_('email address'), unique=True)

#     #! Here we are defining the USERNAME_FIELD as email and REQUIRED_FIELDS as empty list. This is because we are using email as the username and not the username. This is the reason why we set username = None earlier.
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     #! Here we have defined a CustomUserManager named model manager to handle the user model
#     objects = CustomUserManager()


#     def __str__(self):
#         return self.email



# class UserType(models.Model):
#     CUSTOMER = 1
#     SELLER = 2
#     TYPE_CHOICES = (
#         (SELLER, 'Seller'),
#         (CUSTOMER, 'Customer')
#     )

#     id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, primary_key=True)

#     def __str__(self):
#         return self.get_id_display()
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    #* Here we are defining is_customer and is_seller using 3 approaches
    #! Approach 1
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default = False)
    #! Approach 2
    # type = (
    #     (1, 'Seller'),
    #     (2, 'Customer')
    # )
    # user_type = models.IntegerField(choices = type, default=1)
    #! Approach 3
    # usertype = models.ManyToManyField(UserType)

    #! Here we are defining the USERNAME_FIELD as email and REQUIRED_FIELDS as empty list. This is because we are using email as the username and not the username. This is the reason why we set username = None earlier.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    #! Here we have defined a CustomUserManager named model manager to handle the user model
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=1000)


class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gst = models.CharField(max_length=10)
    warehouse_location = models.CharField(max_length=1000)
    
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
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices, default=1)


class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    # user = models.ManyToManyField(User)
    deal_name = models.CharField(max_length=255)
