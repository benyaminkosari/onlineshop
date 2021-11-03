from django.urls import path, include
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductList.as_view(),name='products-view'),
    path('products/add/',views.CreateProduct.as_view(),name='products-add'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(),name='products-detail'),
    path('products/<slug:slug>/add_to_cart/',views.add_to_cart,name='add-to-cart-view'),
    path('products/<slug:slug>/decrease_from_cart/',views.decrease_from_cart,name='decrease-from-cart-view'),
    path('products/<slug:slug>/remove_from_cart/',views.remove_from_cart,name='remove-from-cart-view'),
    path('products/delete/<slug:slug>/',views.DeleteProduct.as_view(),name='products-delete'),
    path('category/<slug:slug>',views.CategoryView.as_view(),name='category-view'),
    path('carts/', views.CartList.as_view(),name='carts-view'),
    path('carts/<int:pk>/',views.CartDetail.as_view(),name='carts-detail'),
    # path('orders/', views.OrderList.as_view(),name='orders-view'),
    path('orders/<int:pk>/',views.OrderDetail.as_view(),name='orders-detail'),
    # path('publish/',views.PublishList.as_view(),name='publish-view'),
    # path('publish/<slug:slug>/',views.PublishView.as_view(),name='publishing'),
    path('payment/<int:pk>/',views.PaymentView,name='payment-view'),
    path('wishlist/<slug:slug>',views.WishListView.as_view(),name='wishlist-view'),
    path('wishlist/add/<slug:slug>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/remove/<slug:slug>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('checkout/',views.CheckoutTemplateView.as_view(),name='checkout-view'),
]
