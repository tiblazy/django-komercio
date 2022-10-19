from rest_framework import serializers

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['id', 'last_login', 'groups', 'user_permissions', 'email', 'is_staff',]
        extra_kwargs = {
            'is_seller': {'required': True,},
            'password': {'write_only': True,},
        }

    def create(self, validated_data: dict) -> dict:
        account = Account.objects.create_user(**validated_data)
        
        return account
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)