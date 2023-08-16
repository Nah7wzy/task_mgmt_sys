from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from project.models import Project, ProjectItems

from project.serializers import CreateProjectSerializer, ProjectDetailSerializer, ProjectItemsSerializer
from task.models import Task
# Create your views here.

class CreateProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateProjectSerializer(data=request.data)
        serializer.context['owner'] = request.user
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProjectView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        items = Project.objects.filter(owner=user_id)
        serializer = ProjectDetailSerializer(items, many=True)
        serializer.context['request'] = request

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, Project_id):
        item = get_object_or_404(Project, id=Project_id)
        serializer = ProjectDetailSerializer(item)
        serializer.context['request'] = request

        return Response(data=serializer.data)

    def delete(self, request, Project_id):
        Project = None
        try:
            Project = Project.objects.get(id=Project_id)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if Project.owner.id == request.user.id:
            Project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProjectItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectItemsSerializer(data=request.data)
        serializer.context['request'] = request

        if serializer.is_valid():
            Project = None
            try:
                Project = serializer.validated_data['Project_id']
                song = serializer.validated_data['task_id']
            except (Project.DoesNotExist, Task.DoesNotExist) as error:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.user.id != Project.owner.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = ProjectItemsSerializer(data=request.data)
        serializer.context['request'] = request
        Project_item = None
        if serializer.is_valid():
            Project_item = ProjectItems.objects.get(
                Project_id=serializer.validated_data['Project_id'], task_id=serializer.validated_data['task_id'])

            if request.user.id != serializer.validated_data['Project_id'].owner.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            Project_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
