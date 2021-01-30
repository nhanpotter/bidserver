from django.urls import path

from .views import ShopBidItemCreateAPIView, ShopBidItemEditAPIView, ShopViewShopBidItemAPIView, ShopViewTokenAPIView, \
    UserProposeBidAPIView, UserViewShopBidItemAPIView, UserViewTokenAPIView, UserViewWinItem

urlpatterns = [
    path('shop/token/', ShopViewTokenAPIView.as_view(), name='shop_token'),
    path('shop/view/', ShopViewShopBidItemAPIView.as_view(), name='shop_view_shop_item'),
    path('shop/create/', ShopBidItemCreateAPIView.as_view(), name='shop_create'),
    path('shop/edit/', ShopBidItemEditAPIView.as_view(), name='shop_edit'),

    path('user/token/', UserViewTokenAPIView.as_view(), name='user_token'),
    path('user/view/', UserViewShopBidItemAPIView.as_view(), name='user_view_shop_item'),
    path('user/bid/', UserProposeBidAPIView.as_view(), name='user_bid'),
    path('user/win/', UserViewWinItem.as_view(), name='user_win_item'),
]
