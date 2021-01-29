from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Shop
from .serializers import ShopSerializer


class ShopViewTokenAPIView(APIView):
    def get(self, request, format=None):
        if 'shop_id' not in request.GET:
            return Response(
                {'error': ['Need to provide shop_id']},
                status=status.HTTP_400_BAD_REQUEST)

        shop_id = request.GET['shop_id']
        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            shop = Shop.objects.create(shop_id=shop_id)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)
