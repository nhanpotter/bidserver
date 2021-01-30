from django.urls import path

from .views import ShopBidItemCreateAPIView, ShopBidItemEditAPIView, ShopViewShopBidItemAPIView, ShopViewTokenAPIView, \
    UserProposeBidAPIView, UserViewBidItemAPIView, UserViewBidItemPersonalAPIView, UserViewPerBidItemAPIView, \
    UserViewShopBidItemAPIView, UserViewTokenAPIView, UserViewWinItemAPIView, ShopViewAllAPIView, ShopViewItemAPIView, \
    UserNotificationAPIView

urlpatterns = [
    path('shop/token/', ShopViewTokenAPIView.as_view(), name='shop_token'),
    path('shop/view/', ShopViewShopBidItemAPIView.as_view(), name='shop_view_shop_item'),
    path('shop/create/', ShopBidItemCreateAPIView.as_view(), name='shop_create'),
    path('shop/edit/', ShopBidItemEditAPIView.as_view(), name='shop_edit'),
    path('shop/view_all/', ShopViewAllAPIView.as_view(), name='shop_view_all'),
    path('shop/view_item/', ShopViewItemAPIView.as_view(), name='shop_view_item'),

    path('user/info/', UserViewTokenAPIView.as_view(), name='user_info'),
    path('user/view_by_shop/', UserViewShopBidItemAPIView.as_view(), name='user_view_shop_item'),
    path('user/bid/', UserProposeBidAPIView.as_view(), name='user_bid'),
    path('user/win/', UserViewWinItemAPIView.as_view(), name='user_win_item'),
    path('user/view_all/', UserViewBidItemAPIView.as_view(), name='user_view_item'),
    path('user/view_all_personal/', UserViewBidItemPersonalAPIView.as_view(), name='user_view_all_personal'),
    path('user/view_per_item/', UserViewPerBidItemAPIView.as_view(), name='user_view_per_item'),

    path('user/notification/', UserNotificationAPIView.as_view(), name='notification'),
]
