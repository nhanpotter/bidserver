import pytz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Shop, User, BidItem
from .serializers import ShopSerializer, UserSerializer, BidItemSerializer
from django.utils import timezone
import datetime

from .utils import *


class ShopViewTokenAPIView(APIView):
    def get(self, request, format=None):
        shop_id = request.query_params.get('shop_id', default=None)
        if shop_id is None:
            return Response(
                {'error': ['Need to provide shop_id']},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            shop = Shop.objects.create(shop_id=shop_id)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShopViewShopBidItemAPIView(APIView):
    def get(self, request, format= None):
        shop_id= request.query_params.get('shop_id', default=None)
        if shop_id is None:
            return Response(
                {'error': ['Need to provide shop_id']},
                status=status.HTTP_400_BAD_REQUEST)
        unix_release_date = request.query_params.get('release_date', default=None)
        release_date= toISO(unix_release_date)
        test= toUnix(release_date)
        if release_date is None:
            return Response(
                {'error': ['Need to provide release_date']},
                status=status.HTTP_400_BAD_REQUEST)
        item_list = BidItem.objects.filter(shop_id=shop_id, release_date=release_date)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewTokenAPIView(APIView):
    def get(self,request, format=None):
        user_id= request.query_params.get('user_id', default= None)
        if user_id is None:
            return Response(
                {'error':['Need to provide user_id']},
                status= status.HTTP_400_BAD_REQUEST
            )
        try:
            user= User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user= User.objects.create(user_id=user_id)
        serializer= UserSerializer(user)
        return Response(serializer.data, status= status.HTTP_200_OK)

class UserViewShopBidItemAPIView(APIView):
    def get(self,request, format=None):
        shop_id= request.query_params.get('shop_id', default=None)
        if shop_id is None:
            return Response({'error':['Need to provide shop_id']}, status= status.HTTP_400_BAD_REQUEST)
        now= timezone.now().date()
        unix= toUnix(now)
        test_unix= toISO(unix)
        item_list= BidItem.objects.filter(shop_id=shop_id, release_date= now)
        serializer= BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)


