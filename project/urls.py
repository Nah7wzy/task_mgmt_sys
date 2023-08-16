from django.urls import path
from .views import ProjectItemsView, ProjectView, CreateProjectView, UserProjectView

urlpatterns = [
    path('create/', CreateProjectView.as_view()),
    path('add/', ProjectItemsView.as_view()),
    path('remove/', ProjectItemsView.as_view()),
    path('delete/<str:project_id>/', ProjectView.as_view()),
    path('<str:project_id>/', ProjectView.as_view()),
    path('user_project/<str:user_id>/', UserProjectView.as_view()),
]