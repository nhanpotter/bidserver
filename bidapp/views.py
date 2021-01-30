from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BidItem, BidTransaction, Shop, User
from .serializers import BidItemCreateSerializer, BidItemEditSerializer, BidTransactionSerializer, ShopSerializer, \
    ShopViewShopBidItemQuerySerializer, ShopViewTokenQuerySerializer, UserViewShopBidItemQuerySerializer, \
    UserViewWinQuerySerializer
from .serializers import BidItemSerializer, UserSerializer, UserViewBidItemSerializer


class ShopViewTokenAPIView(APIView):
    def get(self, request, format=None):
        query_serializer = ShopViewTokenQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        shop_id = query_serializer.validated_data.get('shop_id')
        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            shop = Shop.objects.create(shop_id=shop_id)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopViewShopBidItemAPIView(APIView):
    def get(self, request, format=None):
        query_serializer = ShopViewShopBidItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = query_serializer.validated_data
        shop_id = validated_data.get('shop_id')
        release_date = validated_data.get('release_date')
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
        query_serializer = UserViewShopBidItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        shop_id = query_serializer.validated_data.get('shop_id')
        today = timezone.localtime().date()
        item_list = BidItem.objects.filter(shop_id=shop_id, release_date=today)
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProposeBidAPIView(APIView):
    def post(self, request, format=None):
        # Create user if not exists
        user_id = request.data.get('user')
        if user_id is not None:
            User.objects.get_or_create(user_id=user_id)

        serializer = BidTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        item_id = validated_data.get('item_id')
        shop_id = validated_data.get('shop_id')
        item = BidItem.objects.get(item_id=item_id, shop__shop_id=shop_id)
        token_threshold = item.token_threshold
        token_bid = validated_data.get('token_bid')
        user = validated_data.get('user')

        # Check if user has enough token to bid
        if token_bid > user.token:
            return Response({'error': ['insufficient token']},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if item release date is today
        today = timezone.localtime().date()
        if item.release_date != today:
            return Response({'error': ['item release_date not today']},
                            status=status.HTTP_400_BAD_REQUEST)

        if token_bid > token_threshold:
            return Response({'error': ['token bid > token threshold']},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if user overbid previous token bid
        outbid_user = None
        current_max_bid = 0
        transaction_qs = BidTransaction.objects.filter(item=self).order_by('token_bid')
        if len(transaction_qs) != 0:
            last_transaction = transaction_qs.last()
            outbid_user = last_transaction.user
            current_max_bid = last_transaction.token_bid

        if token_bid < token_threshold and token_bid <= current_max_bid:
            return Response({'error': ['token bid must > max bid']},
                            status=status.HTTP_400_BAD_REQUEST)

        # Deduct user token
        user.token = user.token - token_bid
        user.save()
        # Create Bid Transaction
        create_time = int(timezone.now().timestamp())
        serializer.save(item=item, create_time=create_time)

        if outbid_user is not None and current_max_bid < token_threshold:
            outbid_user.token = outbid_user.token + current_max_bid
            outbid_user.save()

        if outbid_user != user:
            # TODO: Push notification to user got outbid
            pass

        return Response(status=status.HTTP_201_CREATED)


class UserViewWinItem(APIView):
    def get(self, request, format=None):
        query_serializer = UserViewWinQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = query_serializer.validated_data.get('user_id')
        item_list = BidItem.objects.filter(winner=user_id)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewBidItemAPIView(APIView):
    def get(self, request, format=None):
        serializer = UserViewBidItemSerializer(Shop.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
