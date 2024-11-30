# Create your models here.

from django.db import models

class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class EmployeeProfile(models.Model):
    # Link to the existing Employee model
    employee = models.OneToOneField(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='profile' 
    )
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ])
    role = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Profile of {self.employee.username}"
