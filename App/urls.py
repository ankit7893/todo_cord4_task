from django.contrib import admin
from django.urls import path, include
from . views import *
urlpatterns = [
    path('' , include('accounts.urls')), 
    path('list',TodoList.as_view(), name='todolistview'),
    path('listedit/<int:pk>',TodoListEdit.as_view()),
    path('list-delete/<int:pk>',TodoListDelete.as_view(), name='todolistdeleteview'),
    path('list-share/<int:pk>',TodoListShare.as_view()),
]