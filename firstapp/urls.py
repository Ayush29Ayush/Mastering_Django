from django.urls import path, include
from . import views

urlpatterns = [
    # path('index/', views.index, name="index"),
    path('index/', views.Index.as_view(), name="index"),
]
