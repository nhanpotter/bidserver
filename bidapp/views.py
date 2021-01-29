from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BidItem, Shop
from .models import User
from .serializers import BidItemCreateSerializer, BidItemEditSerializer, ShopSerializer
from .serializers import BidItemSerializer, UserSerializer
from .utils import *


class ShopViewTokenAPIView(APIView):
    def get(self, request, format=None):
        shop_id = request.query_params.get('shop_id', default=None)
        if shop_id is None:
            return Response(
                {'error': ['Need to provide shop_id']},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            shop = Shop.objects.create(shop_id=shop_id)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopViewShopBidItemAPIView(APIView):
    def get(self, request, format=None):
        shop_id = request.query_params.get('shop_id', default=None)
        if shop_id is None:
            return Response(
                {'error': ['Need to provide shop_id']},
                status=status.HTTP_400_BAD_REQUEST)
        unix_release_date = request.query_params.get('release_date', default=None)
        if unix_release_date is None:
            return Response(
                {'error': ['Need to provide release_date']},
                status=status.HTTP_400_BAD_REQUEST)
        release_date = to_python_datetime(unix_release_date)
        item_list = BidItem.objects.filter(shop_id=shop_id, release_date=release_date)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewTokenAPIView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user_id', default=None)
        if user_id is None:
            return Response(
                {'error': ['Need to provide user_id']},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User.objects.create(user_id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewShopBidItemAPIView(APIView):
    def get(self, request, format=None):
        shop_id = request.query_params.get('shop_id', default=None)
        if shop_id is None:
            return Response({'error': ['Need to provide shop_id']}, status=status.HTTP_400_BAD_REQUEST)
        now = timezone.now().date()
        item_list = BidItem.objects.filter(shop_id=shop_id, release_date=now)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopBidItemCreateAPIView(APIView):
    def post(self, request, format=None):
        # Create Shop if it does not exist
        shop_id = request.data.get('shop')
        if shop_id is not None:
            Shop.objects.get_or_create(shop_id=shop_id)

        serializer = BidItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopBidItemEditAPIView(APIView):
    def post(self, request, format=None):
        serializer = BidItemEditSerializer(data=request.data)
        if serializer.is_valid():
            # Check if item is already created
            try:
                validated_data = serializer.validated_data
                shop = validated_data.get('shop')
                item_id = request.data.get('item_id')
                BidItem.objects.get(item_id=item_id, shop=shop)
            except BidItem.DoesNotExist:
                return Response(
                    {'error': ['BidItem need to be created first']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
