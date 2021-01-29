from django.urls import path

from .views import ShopViewTokenAPIView

urlpatterns = [
    path('shop/token/', ShopViewTokenAPIView.as_view(), name='shop_token'),
]
