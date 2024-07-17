from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset = Author.objects.all(), many = False)
    class Meta:
        model = Book
        fields = ["id","author", "pdf", "title"]


class AuthorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Password didn't match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()

        #create author instance
        Author.objects.create(user = user)
        return user


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id","user")
        depth = 1


class AuthorLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ("username", "password")



class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
        depth = 1


class AuthorPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, style={"input_type":"password"}, write_only = True)
    password2 = serializers.CharField(max_length=100, style={"input_type":"password"}, write_only = True)
    class Meta:
        model = User
        fields = ("password", "password2")

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        print(user,"user")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password didn't match")
        user.set_password(password)
        user.save()
        Author.objects.get_or_create(user = user)
        return user