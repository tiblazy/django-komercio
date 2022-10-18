from django.contrib.auth import authenticate

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from .models import Account
from .serializers import AccountSerializer, LoginSerializer


class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountLoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        account = authenticate(**serializer.validated_data)
        
        if account:
            token, _ = Token.objects.get_or_create(user=account)
            return Response({'token': token.key,})

        return Response({'detail': 'invalid username or password'}, status.HTTP_400_BAD_REQUEST)
    
class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        max = self.kwargs['num']
        return super().get_queryset().order_by('-date_joined')[0:max]