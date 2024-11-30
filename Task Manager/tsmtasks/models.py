from django.db import models
from tsmusers.models import Employee,EmployeeProfile

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    STATUS_CHOICES = [
    ('Completed', 'Completed'),
    ('In Progress', 'In Progress'),
    ('Failed', 'Failed'),
    ]

    task_name = models.CharField(max_length=255, verbose_name="Task Name")
    task_description = models.TextField(verbose_name="Task Description")
    assigned_employees = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="tasks")

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, verbose_name="Priority")
    due_date = models.DateField(verbose_name="Due Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    
    def __str__(self):
        return self.task_name
