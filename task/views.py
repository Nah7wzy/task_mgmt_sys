from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView, RetrieveAPIView
from .models import Notification, Task
from .serializers import TaskSerializer 
from .permissions import IsTaskCreatorOrAssignedUser
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.utils import timezone
from datetime import timedelta

def create_due_date_notifications(task):
    # Calculate the threshold for upcoming due dates
    threshold = timezone.now() + timedelta(days=2)

    if task.due_date <= threshold:
        notification_message = f"Task '{task.title}' is due on {task.due_date}."
        Notification.objects.create(user=task.created_by, task=task, message=notification_message)

def user_assigned_notification(task):
    notification_message = f"Task '{task.title}' is assigned to '{task.assigned_to}."
    Notification.objects.create(user=task.assigned_to, task=task, message=notification_message)



class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_due_date_notifications(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignUserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({"error": "Missing 'user_id'"}, status=status.HTTP_400_BAD_REQUEST)

       
        task.assigned_to = user_id
        task.save()
        user_assigned_notification(task)

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsTaskCreatorOrAssignedUser]

    queryset = Task.objects.all() 
    # destroy api view performs delete automatically

class TaskView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer  
