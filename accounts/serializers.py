from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        many=True,
        required=False
    )
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only':True}}

    def create(self, validated_data):
        username = validated_data.pop('username')
        #email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(username, '', password)
        #user.update(**validated_data)

        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ChangePWSerializer(serializers.Serializer):
    """
    修改密码
    """
    password = serializers.CharField(max_length=20, min_length=6,
            required=True)
    new_password = serializers.CharField(max_length=20, min_length=6,
            required=True)

    def validate(self, data):
        user = self.context.get('user')

        if not check_password(data['password'], user.password):
            raise serializers.ValidationError({'password':'原始密码错误'})

        return data

    def create(self, validated_data):
        user = self.context.get('user')
        user.set_password(validated_data['new_password'])
        user.save()

        return validated_data


class ResetPWSerializer(serializers.Serializer):
    """
    重置密码
    """
    user = serializers.IntegerField(required=True)
    password = serializers.CharField(max_length=20, min_length=6,
            required=True)

    def validate(self, data):
        if not User.objects.filter(pk=data['user']).exists():
            raise serializers.ValidationError({'user':'用户不存在'})

        return data

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data['user'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data
