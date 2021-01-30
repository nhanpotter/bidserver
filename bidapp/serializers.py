from django.utils import timezone
from rest_framework import serializers

from .models import BidItem, BidTransaction, Shop, User


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
                  'image_url', 'current_max_bid']


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
        item_id = data.get('item_id')
        try:
            BidItem.objects.get(item_id=item_id)
        except BidItem.DoesNotExist:
            raise serializers.ValidationError({'error': ['BidItem not exists']})

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
    shop_id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    token_bid = serializers.IntegerField()
    create_time = serializers.IntegerField(read_only=True)

    def validate(self, data):
        item_id = data.get('item_id')
        shop_id = data.get('shop_id')
        try:
            BidItem.objects.get(item_id=item_id, shop__shop_id=shop_id)
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
