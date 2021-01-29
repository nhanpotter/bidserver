from rest_framework import serializers

from .models import Shop, User, BidItem


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class BidItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= BidItem
        fields= '__all__'
