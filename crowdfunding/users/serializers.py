from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    #New fields as of 13/09
    password = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    phone = serializers.IntegerField()
    image = serializers.URLField(max_length=200)
    country = serializers.CharField(max_length=80) 
    date_created = serializers.DateTimeField()


    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

class CustomUserDetailSerializer(CustomUserSerializer):
    #allows the serializer to perform updates on our model
    def update(self, instance, validated_data): #instance will be the user in question
        instance.email = validated_data.get('email', instance.email) #only giving the user the ability to change their email
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.image = validated_data.get('image', instance.image)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance