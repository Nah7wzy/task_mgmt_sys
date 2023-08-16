from rest_framework import serializers
from user.serializers import UserPublicSerializer

from project.models import Project, ProjectItems
from task.serializers import TaskSerializer

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['owner', 'name', 'id']
        read_only_fields = ['owner', 'id']

    def create(self, validated_data):
        project = Project(
            owner=self.context['owner'],
            name=validated_data['name']
        )

        project.save()
        return project
    
class ProjectItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectItems
        fields = ['project_id', 'task_id']


class ProjectDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'owner', 'items')
        read_only_fields = ['owner', 'id']
        depth = 2

    def get_items(self, obj):
        items = ProjectItems.objects.filter(Project_id=obj.id)
        tasks = []
        for item in items:
            tasks.append(item.task_id)
        return TaskSerializer(tasks, many=True, context=self.context).data

    def get_owner(self, obj):
        return UserPublicSerializer(obj.owner, context=self.context).data