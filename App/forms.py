from dataclasses import fields
from django.forms import ModelForm
from . models import *


class TodoForm(ModelForm):
    class Meta:
        model = ToDo
        exclude = ['user']
