from django.contrib import admin
from django.urls import path

from Log.views import *

urlpatterns = [
    path('shared-edit/<int:pk>',TodoSharedListEdit.as_view()),
    path('log',LogList.as_view()),
    path('approval-list/<int:pk>',ApprovalList.as_view()),
    path('approval-status/<int:log_pk>/<str:status>',ApprovalStatusChange.as_view()),


]