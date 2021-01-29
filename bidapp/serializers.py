from rest_framework import serializers

from .models import BidItem, Shop, User
from .utils import to_unix, to_python_datetime


class UnixDateField(serializers.DateField):
    def to_representation(self, value):
        return to_unix(value)

    def to_internal_value(self, value):
        return to_python_datetime(value)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BidItemSerializer(serializers.ModelSerializer):
    release_date = UnixDateField()

    class Meta:
        model = BidItem
        fields = '__all__'


class BidItemCreateSerializer(serializers.ModelSerializer):
    release_date = UnixDateField()

    class Meta:
        model = BidItem
        fields = '__all__'
        read_only_fields = ['winner']

    def validate(self, data):
        item_id = data.get('item_id')
        shop = data.get('shop')
        if BidItem.objects.filter(item_id=item_id, shop=shop).exists():
            raise serializers.ValidationError({'error': 'item already created'})
        return data

    def create(self, validated_data):
        created = BidItem.objects.create(**validated_data)
        return created


class BidItemEditSerializer(serializers.ModelSerializer):
    release_date = UnixDateField()

    class Meta:
        model = BidItem
        fields = '__all__'
        read_only_fields = ['winner']
        extra_kwargs = {
            'token_threshold': {'required': False},
            'release_date': {'required': False},
            'name': {'required': False},
            'description': {'required': False},
            'original_price': {'required': False},
            'discount_price': {'required': False},
            'image_url': {'required': False},
        }

    def save(self):
        validated_data = self.validated_data
        item_id = validated_data.get('item_id')
        shop = validated_data.get('shop')
        instance = BidItem.objects.get(item_id=item_id, shop=shop)

        instance.token_threshold = validated_data.get('token_threshold', instance.token_threshold)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.original_price = validated_data.get('original_price', instance.original_price)
        instance.discount_price = validated_data.get('discount_price', instance.discount_price)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance
