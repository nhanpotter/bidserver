from django.urls import path

from .views import ShopViewTokenAPIView, UserViewTokenAPIView, UserViewShopBidItemAPIView, ShopViewShopBidItemAPIView

urlpatterns = [
    path('shop/token/', ShopViewTokenAPIView.as_view(), name='shop_token'),
    path('user/token/', UserViewTokenAPIView.as_view(), name='user_token'),
    path('user/view/', UserViewShopBidItemAPIView.as_view(), name='user_view_shop_item'),
    path('shop/view/', ShopViewShopBidItemAPIView.as_view(), name= 'shop_view_shop_item'),
]
