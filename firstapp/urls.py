from django.urls import path, include
from . import views

urlpatterns = [
    # path('index/', views.index, name="index"),
    path('', views.Index.as_view(), name="index"),
    path('contactus/', views.contactus, name="contact"),
]
