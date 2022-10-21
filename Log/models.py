from email.policy import default
from django.db import models
from App.models import ToDo
from django.contrib.auth.models import User
from datetime import date

 
# Create your models here.

class TaskLog(models.Model):
    task = models.ForeignKey(ToDo, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=500)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    due_date = models.DateField()
    change_date = models.DateField(default=date.today())
    result_status = models.CharField(max_length=20, default="inprogress")
