from django.shortcuts import render

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserDetailSerializer
from .permissions import IsOwnerOrReadOnly 

class CustomUserList(APIView):
    def get(self,request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class CustomUserDetail(APIView):
    #So only after log in the user can change its details
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,  IsOwnerOrReadOnly] 

    def get_object(self,pk):
        try:
            user=CustomUser.objects.get(pk=pk) #gets the user with the relevant pk from the database
            self.check_object_permissions(self.request, user) #checks the permissions
            return user

        except CustomUser.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

#Trying to create a put method to allow the user to update its details
#13.09: it worked, changed superuser email when logged in as superuser
#tried to update a user that did not exist and got the corresponding 404 not found
#Problem: it let me change the email of another user
#Update: problem above solved, had forgotten to add line 31 to check object permissions
#Also tried to change the username field, and it did not work because it is not defined in the serializer for update

    def put(self, request, pk): #put is used for putting some new info on a row on the database, as opposed to creating a whole new row
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserDetailSerializer(
            instance=user,
            data=data,
            partial=True #this makes it ok if only some data is updated
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) #this is not on the original pdf, added with Ollie
        
        return Response(serializer.errors) #it is good practice to always give a return when the data is not valid
        