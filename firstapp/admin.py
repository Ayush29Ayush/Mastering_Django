from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from firstapp.forms import CustomUserChangeForm, CustomUserCreationForm

from firstapp.models import Product, Cart, ProductInCart, Order, Deal, CustomUser

# from firstapp.models import Product, Cart, ProductInCart, Order


class ProductInCartInline(admin.TabularInline):
    model = ProductInCart


class CartInline(admin.TabularInline):
    model = Cart  # one to one foreign key


class DealInline(admin.TabularInline):
    model = Deal.user.through

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)



# class UserAdmin(UserAdmin):
#     model = User

#     #! To specify which all fields to display when the user clicks on the "Users" object in admin page
#     list_display = (
#         "username",
#         "get_cart",
#         "email",
#         "is_staff",
#         "is_active",
#     )
#     #! This is for sidebar filter box
#     list_filter = (
#         "username",
#         "email",
#         "is_staff",
#         "is_active",
#     )
#     #! When you click and open the details page of a certain user, you will show these fieldsets.
#     fieldsets = (
#         # (None, {'fields': ('username', 'password')}),
#         (
#             "This will be the heading for USER basic details -> set by AYUSH",
#             {"fields": ("username", "password")},
#             # {"classes": ("collapse",), "fields": ("username", "password")},
#         ),
#         (
#             "Permissions",
#             {
#                 "classes": ("collapse",),
#                 "fields": ("is_staff", "is_active", "is_superuser"),
#             },
#         ),
#         (
#             "Important dates",
#             {"classes": ("collapse",), "fields": ("last_login", "date_joined")},
#         ),
#         # ('Carts', {'fields': ('get_cart',)}),
#         (
#             "Advanced options",
#             {"classes": ("collapse",), "fields": ("groups", "user_permissions")},
#         ),
#     )

#     #! These fields will be shown on create user page
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),  # class for CSS
#                 "fields": (
#                     "username",
#                     "password1",
#                     "password2",
#                     "is_staff",
#                     "is_active",
#                     "is_superuser",
#                     "groups",
#                 ),
#             },
#         ),
#     )
#     inlines = [CartInline, DealInline]

#     # This func is used to show which user is linked to which cart as they have foreign key relationship
#     def get_cart(self, obj):
#         return obj.cart  # return through reverse related relationship

#     search_fields = ("email",)  # search_filter for search bar
#     ordering = ("email",)


@admin.register(Cart)  # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = (
        "user",
        "staff",
        "created_on",
    )  # here user__is_staff will not work
    list_filter = (
        "user",
        "created_on",
    )
    # fields = ('staff',)           # either fields or fieldset
    #! Benifit of fieldsets is it allows grouping of related fields together and we can set properties like collapse etc and can set headings
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "created_on",
                )
            },
        ),  # only direct relationship no nested relationship('__') ex. user__is_staff
        # ('User', {'fields': ('staff',)}),
    )
    inlines = (ProductInCartInline,)

    # To display only in list_display
    def staff(self, obj):
        return obj.user.is_staff

    # staff.empty_value_display = '???'
    staff.admin_order_field = "user__is_staff"  # Allows column order sorting
    staff.short_description = "Staff User"  # Renames column head

    # Filtering on side - for some reason, this works
    list_filter = [
        "user__is_staff",
        "created_on",
    ]  # with direct foreign key(user) no error but not shown in filters, with function error
    # ordering = ['user',]
    search_fields = [
        "user__username"
    ]  # with direct foreign key no error but filtering not possible directly


class DealAdmin(admin.ModelAdmin):
    inlines = [
        DealInline,
    ]
    exclude = ("user",)


#! Unregister the default User model admin and regisiter the custom UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


# Register your models here.
admin.site.register(Product)
# admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(Order)
admin.site.register(Deal, DealAdmin)
