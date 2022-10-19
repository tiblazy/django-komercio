from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication

from .models import Product
from .serializers import ProductBasicSerializer, ProductDetailsSerializer
from .mixins import SerializerByMethodMixin
from .permissions import SellerPermission, SellerOwnerPermission

class ProductView(SerializerByMethodMixin, ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_map = {'GET': ProductBasicSerializer, 'POST': ProductDetailsSerializer,}
    authentication_classes = [TokenAuthentication]
    permission_classes = [SellerPermission,]
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
                                        
class ProductRetrieveView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [SellerOwnerPermission,]
    