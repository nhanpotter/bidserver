from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BidItem, Shop, User, Notification
from .serializers import BidItemCreateSerializer, BidItemEditSerializer, BidTransactionSerializer, ShopSerializer, \
    ShopViewShopBidItemQuerySerializer, ShopViewTokenQuerySerializer, UserViewBidItemPersonalQuerySerializer, \
    UserViewBidItemPersonalSerializer, UserViewPerBidItemQuerySerializer, UserViewShopBidItemQuerySerializer, \
    UserViewWinQuerySerializer, ShopViewAllQuerySerializer, ShopViewPerItemQuerySerializer, \
    UserNotificationQuerySerializer, NotificationSerializer, UserViewPastItemQuerySerializer
from .serializers import BidItemSerializer, UserSerializer, UserViewBidItemSerializer


class ShopViewTokenAPIView(APIView):
    @csrf_exempt
    def get(self, request):
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
    @csrf_exempt
    def get(self, request):
        query_serializer = ShopViewShopBidItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = query_serializer.validated_data
        shop_id = validated_data.get('shop_id')
        release_date = validated_data.get('release_date')
        item_list = BidItem.objects.filter(shop_id=shop_id, release_date=release_date)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopBidItemCreateAPIView(APIView):
    @csrf_exempt
    def post(self, request):
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
    @csrf_exempt
    def post(self, request):
        serializer = BidItemEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopViewAllAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        # TODO: Create shop if not init
        query_serializer = ShopViewAllQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        shop_id = query_serializer.validated_data.get('shop_id')
        item_qs = BidItem.objects.filter(shop__shop_id=shop_id).order_by('release_date')
        serializer = BidItemSerializer(item_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopViewItemAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        query_serializer = ShopViewPerItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item_id = query_serializer.validated_data.get('item_id')
        try:
            item = BidItem.objects.get(item_id=item_id)
        except BidItem.DoesNotExist:
            return Response({'error': 'BidItem not exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BidItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewTokenAPIView(APIView):
    @csrf_exempt
    def get(self, request):
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
    @csrf_exempt
    def get(self, request):
        query_serializer = UserViewShopBidItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        shop_id = query_serializer.validated_data.get('shop_id')
        today = timezone.localtime().date()
        item_list = BidItem.objects.filter(shop_id=shop_id, release_date=today)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProposeBidAPIView(APIView):
    @csrf_exempt
    def post(self, request):
        # Create user if not exists
        user_id = request.data.get('user')
        if user_id is not None:
            User.objects.get_or_create(user_id=user_id)

        serializer = BidTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        item_id = validated_data.get('item_id')
        item = BidItem.objects.get(item_id=item_id)
        token_threshold = item.token_threshold
        current_token_bid = validated_data.get('token_bid')
        user = validated_data.get('user')

        # TODO: Check if current time > 23:59:00

        # Check if user has enough token to bid
        if current_token_bid > user.token_balance:
            return Response({'error': ['insufficient token']},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if item release date is today
        today = timezone.localtime().date()
        if item.release_date != today:
            return Response({'error': ['item release_date not today']},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if user bid <= threshold
        if current_token_bid > token_threshold:
            return Response({'error': ['token bid > token threshold']},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if user has enough token to outbid previous token bid
        current_max_bid = item.current_max_bid
        if current_token_bid < token_threshold and current_token_bid <= current_max_bid:
            return Response({'error': ['token bid must > max bid']},
                            status=status.HTTP_400_BAD_REQUEST)

        # Deduct user token
        user.token_balance = user.token_balance - current_token_bid
        user.save()

        # Refund user got outbid
        outbid_user = None
        max_bid_users = item.get_max_bid_users()
        if len(max_bid_users) == 1:
            outbid_user = max_bid_users[0]
        if outbid_user is not None and current_max_bid < token_threshold:
            outbid_user.token_balance = outbid_user.token_balance + current_max_bid
            outbid_user.save()

        # Send notification to user got outbid
        if outbid_user is not None and user != outbid_user:
            title = "Outbid"
            content = item.get_outbid_content()
            create_time = int(timezone.now().timestamp())
            Notification.objects.create(item=item, user=outbid_user,
                                        title=title, content=content,
                                        create_time=create_time)
            outbid_user.unseen_noti_no = outbid_user.unseen_noti_no + 1
            outbid_user.save()

        # Create Bid Transaction
        create_time = int(timezone.now().timestamp())
        serializer.save(item=item, create_time=create_time)

        return Response({}, status=status.HTTP_201_CREATED)


class UserViewWinItemAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        query_serializer = UserViewWinQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = query_serializer.validated_data.get('user_id')
        item_list = BidItem.objects.filter(winner=user_id)
        serializer = BidItemSerializer(item_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewBidItemAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        serializer = UserViewBidItemSerializer(Shop.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewBidItemPersonalAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        query_serializer = UserViewBidItemPersonalQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = query_serializer.validated_data.get('user_id')
        today = timezone.localtime().date()
        item_list = BidItem.objects.filter(release_date=today)
        serializer = UserViewBidItemPersonalSerializer(item_list, many=True,
                                                       context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewPerBidItemAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        query_serializer = UserViewPerBidItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = query_serializer.validated_data
        user_id = validated_data.get('user_id')
        item_id = validated_data.get('item_id')
        try:
            item = BidItem.objects.get(item_id=item_id)
        except BidItem.DoesNotExist:
            return Response({'error': 'BidItem not exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserViewBidItemPersonalSerializer(item, context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserNotificationAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        query_serializer = UserNotificationQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = query_serializer.validated_data.get('user_id')
        user = User.objects.get(user_id=user_id)
        user.unseen_noti_no = 0
        user.save()

        notifications = Notification.objects.filter(user__user_id=user_id).order_by('-create_time')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewPastItemAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        query_serializer = UserViewPastItemQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = query_serializer.validated_data.get('user_id')
        today = timezone.localtime().date()
        item_list = BidItem.objects.filter(release_date__lt=today)
        serializer = UserViewBidItemPersonalSerializer(item_list, many=True,
                                                       context={'user_id': user_id})
        return Response(serializer.data, status=status.HTTP_200_OK)
