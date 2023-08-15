from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import UserManager
from django.conf import settings
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True,)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def save(self, *args, **kwargs):
            created = not self.pk  # Check if the user is being created or updated
            super().save(*args, **kwargs)

            if created:
                if self.is_employee:
                    Employee.objects.create(user=self)
                elif self.is_employer:
                    Employer.objects.create(user=self)
    
class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, primary_key=True, related_name='employee')
    
class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True, related_name='employer')
    city = models.CharField(max_length=255)
      
class Jobapplication(models.Model):
    EXPERIENCE_CHOICES = [
        ('4', 'No experience'),
        ('3', 'From 1 to 3 years'),
        ('2', 'From 3 to 6 years'),
        ('1', 'More than 6 years'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('5', 'Full - Time'),
        ('4', 'Part - Time'),
        ('3', 'Project'),
        ('2', 'Volunteering'),
        ('1', 'Internship'),
    ]
    
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('rub', 'RUB'),
    ]
    
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='application')
    company_name = models.CharField(max_length=70, null=True)
    job_name = models.CharField(max_length=70)
    location = models.CharField(max_length=30)
    base_salary = models.CharField(max_length=30)
    floor_salary = models.CharField(max_length=30)
    experience = models.CharField(max_length=12, choices=EXPERIENCE_CHOICES)
    job_description = models.TextField(max_length=1000, validators=[MinLengthValidator(155)])
    job_type = models.CharField(max_length=12, choices=JOB_TYPE_CHOICES)
    currency = models.CharField(choices=CURRENCY_CHOICES, null=True)
    email = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    
class Response(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_response', null=True)
    application = models.ForeignKey(Jobapplication, on_delete=models.CASCADE, related_name='responses', null=True)
    file = models.FileField(upload_to='uploads')
    message = models.TextField(max_length=500)
    
