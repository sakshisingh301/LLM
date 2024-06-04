from django.urls import path
from .views import  ItemCreate

urlpatterns = [

    path('items/create/', ItemCreate.as_view())
]