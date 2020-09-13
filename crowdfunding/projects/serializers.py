from rest_framework import serializers
from .models import Project
from .models import Pledge


class PledgeSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    amount = serializers.IntegerField()
    comment = serializers.CharField(max_length=200)
    anonymous = serializers.BooleanField()
    supporter = serializers.CharField(max_length=200)
    project_id = serializers.IntegerField() #cannot hand over the project object

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None) 
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    owner = serializers.ReadOnlyField(source='owner.id') #owner.id gets setup in views.py
    

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

class ProjectDetailSerializer(ProjectSerializer): #inherits everything from ProjectSerializer class above. We are creating this so the pledges info is only avail when you access the project details view
    pledges = PledgeSerializer(many=True, read_only=True) #read_only so when you are viewing the project you can also view the pledges but you cannot change the pledges

    #allows the serializer to perform updates on our model
    def update(self, instance, validated_data): #instance will be the project we are taking
        instance.title = validated_data.get('title', instance.title) # this would change the project title with new data, if none is given then the original title stays because instance.title is the default value
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        #instance.owner = validated_data.get('owner', instance.owner)
        instance.owner = instance.owner #if this is implemented then the owner of the project cannot be changed
        instance.save()
        return instance
