from django.contrib.auth import authenticate, hashers

from rest_framework.views import Response, status
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination

from .models import Account
from .serializers import AccountSerializer, LoginSerializer
from .permissions import AccountOwnerPermission

class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = PageNumberPagination
    
class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        max = self.kwargs['num']
        return super().get_queryset().order_by('-date_joined')[0:max]
    
class AccountUpdateView(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [AccountOwnerPermission]
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'    
    
    def perform_update(self, serializer):
        password = self.get_object().password

        if 'password' in self.request.data.keys():
            password = hashers.make_password(self.request.data['password'])

        return serializer.save(data=self.request, password=password, is_active=True)                
class ManagerView(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'    

    def perform_update(self, serializer):
        password = self.get_object().password

        if 'password' in self.request.data.keys():
            password = hashers.make_password(self.request.data['password'])

        return serializer.save(data=self.request, password=password)

        
class AccountLoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        account = authenticate(**serializer.validated_data)
        
        if account:
            token, _ = Token.objects.get_or_create(user=account)
            return Response({'token': token.key,})

        return Response({'detail': 'invalid username or password'}, status.HTTP_400_BAD_REQUEST)
