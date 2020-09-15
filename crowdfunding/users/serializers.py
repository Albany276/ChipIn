from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    #New fields as of 13/09
    password = serializers.CharField(write_only = True) #data goes only one way into the database, calling it password makes it recognizable to create_user
    first_name = serializers.CharField(max_length=80)
    last_name = serializers.CharField(max_length=80)
    #phone = serializers.IntegerField(required=False)
    #image = serializers.URLField(max_length=200, required=False)
    #country = serializers.CharField(max_length=80, required=False) 
    #date_created = serializers.DateTimeField()
    #By commenting out the above fields, then the serializer does not expect these fields when a request is created
    #previously this was creating errors if the post request did not have all the expected fields

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data) #changed to create_user rather than create to give us the ability to add the password the field
        #the password does not just get saved as data in the database, it seals it criptographically.

class CustomUserDetailSerializer(CustomUserSerializer):
    #allows the serializer to perform updates on our model
    #These fields are now defined here because they were not defined in the CustomUserSerializer
    #The fact that instance.xx exists mean that if we dont give the serializer any value in those fields then 
    #it will assign whatever it used to have, so in the case of say phone, it would be null
    phone = serializers.IntegerField(required=False)
    image = serializers.URLField(max_length=200, required=False)
    country = serializers.CharField(max_length=80, required=False) 
    date_created = serializers.DateTimeField(read_only = True)
    #if we dont call out these fields in the serializer then they would not be visible from Insomnia even if the fields exist in the database

    def update(self, instance, validated_data): #instance will be the user in question
        instance.email = validated_data.get('email', instance.email) #only giving the user the ability to change their email
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.image = validated_data.get('image', instance.image)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance