from django.forms import ModelForm
from .models import TaskLog


class TaskLogForm(ModelForm):
    class Meta:
        model = TaskLog
        exclude = ['user','task','change_date','result_status']
