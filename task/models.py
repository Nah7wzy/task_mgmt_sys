from django.db import models

from user.models import User

# Create your models here.
#Task: Fields - title, description, due date, status, priority, labels

PRIORITY_CHOICES = (
    ("LOW", "LOW"),
    ("HIGH", "HIGH"),
    ("MEDIUM", "MEDIUM")
)
LABEL_CHOICES = (
    ("WORK", "WORK"),
    ("PERSONAL", "PERSONAL"),
    ("OTHER", "OTHER")
)

STATUS_CHOICES = (
    ("TODO", "TODO"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("DONE", "DONE")
)

class Task(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=20, blank=False, null=False)
    duedate = models.DateField(blank = False, null=False)
    status = models.CharField(max_length=20, choices = STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices = PRIORITY_CHOICES)
    labels = models.CharField(max_length=20, choices = LABEL_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

    from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
