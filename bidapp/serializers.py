from django.utils import timezone
from rest_framework import serializers

from .models import BidItem, BidTransaction, Shop, User, Notification


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ShopViewTokenQuerySerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()


class ShopViewShopBidItemQuerySerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()
    release_date = serializers.DateField()


class UserViewShopBidItemQuerySerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()


class UserViewWinQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class BidItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidItem
        fields = ['item_id', 'shop', 'token_threshold', 'release_date', 'winner',
                  'name', 'description', 'original_price', 'discount_price',
                  'image_url', 'current_max_bid', 'participant_no', 'threshold_bidder_no']


class BidItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidItem
        fields = ['item_id', 'shop', 'token_threshold', 'release_date', 'winner',
                  'name', 'description', 'original_price', 'discount_price',
                  'image_url']
        read_only_fields = ['item_id', 'winner']

    def validate(self, data):
        release_date = data.get('release_date')
        if release_date <= timezone.localtime().date():
            raise serializers.ValidationError({'error': ['release date must > today']})

        return data

    def create(self, validated_data):
        created = BidItem.objects.create(**validated_data)
        return created


class BidItemEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidItem
        fields = ['item_id', 'shop', 'token_threshold', 'release_date', 'winner',
                  'name', 'description', 'original_price', 'discount_price',
                  'image_url']
        read_only_fields = ['shop', 'winner']
        extra_kwargs = {
            'token_threshold': {'required': False},
            'release_date': {'required': False},
            'name': {'required': False},
            'description': {'required': False},
            'original_price': {'required': False},
            'discount_price': {'required': False},
            'image_url': {'required': False},
        }

    def validate(self, data):
        release_date = data.get('release_date')
        if release_date <= timezone.localtime().date():
            raise serializers.ValidationError({'error': ['release date must > today']})

        return data

    def save(self):
        validated_data = self.validated_data
        item_id = validated_data.get('item_id')
        instance = BidItem.objects.get(item_id=item_id)

        instance.token_threshold = validated_data.get('token_threshold', instance.token_threshold)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.original_price = validated_data.get('original_price', instance.original_price)
        instance.discount_price = validated_data.get('discount_price', instance.discount_price)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance


class BidTransactionSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    token_bid = serializers.IntegerField()
    create_time = serializers.IntegerField(read_only=True)

    def validate(self, data):
        item_id = data.get('item_id')
        try:
            BidItem.objects.get(item_id=item_id)
        except BidItem.DoesNotExist:
            raise serializers.ValidationError({'error': ['item does not exists']})

        return data

    def create(self, validated_data):
        item = validated_data.get('item')
        user = validated_data.get('user')
        token_bid = validated_data.get('token_bid')
        create_time = validated_data.get('create_time')

        created = BidTransaction.objects.create(item=item, user=user,
                                                token_bid=token_bid,
                                                create_time=create_time)
        return created


class UserViewBidItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['shop_id', 'items']

    def get_items(self, obj):
        today = timezone.localtime().date()
        items = BidItem.objects.filter(shop=obj, release_date=today)
        serializer = BidItemSerializer(items, many=True)
        return serializer.data


class UserViewBidItemPersonalQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class UserViewBidItemPersonalSerializer(serializers.ModelSerializer):
    user_participated = serializers.SerializerMethodField()
    user_token_bid = serializers.SerializerMethodField()

    class Meta:
        model = BidItem
        fields = ['item_id', 'shop', 'token_threshold', 'release_date', 'winner',
                  'name', 'description', 'original_price', 'discount_price',
                  'image_url', 'current_max_bid', 'participant_no', 'threshold_bidder_no',
                  'user_participated', 'user_token_bid']

    def get_user_participated(self, obj):
        user_id = self.context.get('user_id')
        if BidTransaction.objects.filter(user__user_id=user_id, item=obj).exists():
            return True
        return False

    def get_user_token_bid(self, obj):
        user_id = self.context.get('user_id')
        max_bidders = obj.get_max_bid_users()
        for bidder in max_bidders:
            if bidder.user_id == user_id:
                return obj.current_max_bid
        return None


class UserViewPerBidItemQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    item_id = serializers.IntegerField()


class ShopViewAllQuerySerializer(serializers.Serializer):
    shop_id = serializers.IntegerField()


class ShopViewPerItemQuerySerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class UserNotificationQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserViewPastItemQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()