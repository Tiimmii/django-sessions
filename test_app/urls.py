from django.urls import path
from .views import product_list, product_detail

app_name = 'p'

urlpatterns = [
    path('products/', product_list.as_view(), name=''),
    path('detail/<int:pk>/', product_detail.as_view(), name='detail'),
]