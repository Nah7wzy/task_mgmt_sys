from django.urls import path
from .views import CreateTaskView, AssignUserView, TaskDeleteView, TaskView

urlpatterns = [
    path('create/', CreateTaskView.as_view()),
    path('assign/<str:user_id>/', AssignUserView.as_view()),
    path('delete/<str:task_id>/', TaskDeleteView.as_view()),
    path('<str:id>/', TaskView.as_view()),
]