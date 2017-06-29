from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import I2XUser
from accounts.models import Team


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'id',)
        read_only_fields = ('id',)


class I2XUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    verified = serializers.BooleanField()

    class Meta:
        model = I2XUser
        fields = ('id', 'user', 'verified',)


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)    
    name = serializers.CharField()
    invitation_code = serializers.UUIDField(read_only=True, required=False)

    class Meta:
        model = Team
        fields = ('id', 'name', 'invitation_code',)
        
