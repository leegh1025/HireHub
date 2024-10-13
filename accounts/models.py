from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class InterviewerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)
    
        return self.create_user(email, password, **extra_fields)

class Interviewer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    is_approved = models.BooleanField(default=False) # 승인을 해야 로그인이 가능하게 하기 위해서 둠!
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = InterviewerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

class InterviewTeam(models.Model):
    team_name = models.CharField(max_length=255)
    members = models.ManyToManyField(Interviewer)
    average_score = models.IntegerField(default=0)

    def __str__(self):
        return self.team_name