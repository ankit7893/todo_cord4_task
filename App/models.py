from django.db import models
from django.contrib.auth.models import User
# Create your models here.


'''ToDo model where basic tasks data is saved'''
class ToDo(models.Model):

    STATUS_CHOICES = [
        ('', '-Status-'),
        ('Completed', 'Completed'),
        ('In-progress', 'In-progress')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, help_text='Task Name')
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS_CHOICES, default='In-progress',  max_length=20)
    due_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class TodoShareModal(models.Model):
    task = models.ForeignKey(ToDo, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    permission = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.permission