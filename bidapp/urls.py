from django.urls import path

from .views import ShopBidItemCreateAPIView, ShopBidItemEditAPIView, ShopViewShopBidItemAPIView, ShopViewTokenAPIView, \
    UserProposeBidAPIView, UserViewShopBidItemAPIView, UserViewTokenAPIView, UserViewWinItemAPIView, UserViewBidItemAPIView, \
    UserViewBidItemPersonalAPIView

urlpatterns = [
    path('shop/token/', ShopViewTokenAPIView.as_view(), name='shop_token'),
    path('shop/view/', ShopViewShopBidItemAPIView.as_view(), name='shop_view_shop_item'),
    path('shop/create/', ShopBidItemCreateAPIView.as_view(), name='shop_create'),
    path('shop/edit/', ShopBidItemEditAPIView.as_view(), name='shop_edit'),

    path('user/token/', UserViewTokenAPIView.as_view(), name='user_token'),
    path('user/view_by_shop/', UserViewShopBidItemAPIView.as_view(), name='user_view_shop_item'),
    path('user/bid/', UserProposeBidAPIView.as_view(), name='user_bid'),
    path('user/win/', UserViewWinItemAPIView.as_view(), name='user_win_item'),
    path('user/view_all/', UserViewBidItemAPIView.as_view(), name='user_view_item'),
    path('user/view_all_personal/', UserViewBidItemPersonalAPIView.as_view(), name='user_view_all_personal')
]
