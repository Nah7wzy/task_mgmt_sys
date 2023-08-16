import uuid
from django.db import models

from user.models import User
from task.models import Task

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=150, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ProjectItems(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'project-items'
        constraints = [
            models.UniqueConstraint(
                fields=['project_id', 'task_id'], name='unique project-items')
        ]

    def __str__(self):
        return self.task_id.title