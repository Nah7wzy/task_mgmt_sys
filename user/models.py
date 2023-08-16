import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

  

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    
    objects = UserManager()
    def __str__(self):
        return self.username