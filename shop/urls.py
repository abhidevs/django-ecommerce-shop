from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ShopHome'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContacttUs'),
    path('track/', views.track, name='Track'),
    path('search/', views.search, name='Search'),
    path('product/<int:id>', views.product, name='Product'),
    path('cart/', views.cart, name='Cart'),
    path('updateCart/<str:action>', views.updateCart, name='updateCart'),
    path('checkout/', views.checkout, name='Checkout'),
    path('addAddress/', views.addAddress, name='addAddress'),
    path('editAddress/', views.editAddress, name='editAddress'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:orderId>', views.order, name='order')
]
