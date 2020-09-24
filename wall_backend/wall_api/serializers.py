from rest_framework import serializers
from wall_api.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Creates a new user with a hashed password
        """
        password = validated_data.pop('password')
        new_user = User.objects.create(**validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user


class PostSerializer(serializers.ModelSerializer):
    posted_by = serializers.ReadOnlyField(source='posted_by.username')

    class Meta:
        model = Post
        fields = ['time', 'content', 'posted_by']
