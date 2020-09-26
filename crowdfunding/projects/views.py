from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer
from django.http import Http404, HttpResponse, HttpResponseNotFound
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly 


class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #this definition exists on the rest_framework, only ppl that logged in can update info

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request): 
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user) #this will assign the logged in user as the project owner
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,  IsOwnerOrReadOnly] 


    def get_object(self, pk):
        try:
            project=Project.objects.get(pk=pk) #gets the project with the relevant pk from the database
            self.check_object_permissions(self.request, project)
            return project

        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk): #put is used for putting some new info on a row on the database, as opposed to creating a whole new row
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True #this makes it ok if only some data is updated
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) #this is not on the original pdf, added with Ollie
        
        return Response(serializer.errors) #it is good practice to always give a return when the data is not valid

    ###Trying to create a delete method for projects -
    #13/09: After testing in insomnia it works, only the author of the project can delete it
    #upon deletion you get a http 204 message
    #if you try to delete a project that you did not create you get a 403 error -you dont have permissions to perform this action
    # I think the above happens because of permission classes in line 33
    def delete(self, request, pk):
        project = self.get_object(pk) #get_object already has a 404 if the project is not found
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #this definition exists on the rest_framework, only ppl that logged in can update info
    

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)


   
    def post(self, request):
     # Below we are going to check that the project id exists and also that the creator of the pledge (supporter) is not the project owner
        try: 
            aux2 = request.data["project_id"] #gets project id from the request.data dictionary
            project=Project.objects.get(pk=aux2) #gets the project with the relevant pk from the database
           
            if project.owner == request.user: #checks if the user making the pledge is the same as the owner of the project
               # return Response(status=status.HTTP_204_NO_CONTENT) #if that is the case raise an error
                return HttpResponseNotFound('<h3>you cant pledge to your own project</h3>') #found that you can pass html strings to http response. Had to import httresponse at the top of file

            else: #otherwise if the user making the pledge is not the owner of the project, then save the pledge
                serializer = PledgeSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save(supporter = request.user)

                    #creating a tally of amount pledged
                    project.amount_raised = request.data["amount"] + project.amount_raised #request.data["amount"] gives you the pledge amount 
                    project.save() #this saves it back to the project, you dont need to use the put method, those methods are for ppl interacting with the api

                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Project.DoesNotExist:
            raise Http404




       