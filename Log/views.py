from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from . models import *
from . forms import *
from App.models import ToDo

# Create your views here.

class LogList(View):
    def get(self, request):
        list = TaskLog.objects.filter(task__user=request.user)
        data = {
            'loglist':list
            }
        return render(request, 'log/log.html', data)


class TodoSharedListEdit(View):
    def get(self, request, pk):
        list = ToDo.objects.get(id=pk)
        form = TaskLogForm(instance = list)
        data = {
            'sharedform':form
            }
        return render(request, 'log/sharededit.html', data)

    def post(self, request, pk):
        list = ToDo.objects.get(id=pk)
        form = TaskLogForm(request.POST)
        if form.is_valid():
            form = form.save()
            form.task = list
            form.user = request.user
            form.save()
            print("Done")
        else:
            print("not done")    
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ApprovalList(View):
    def get(self, request, pk):
        list = TaskLog.objects.filter(task__id=pk, result_status='inprogress')
        print(list)
        data = {
            'loglist':list
            }
        return render(request, 'log/Approval.html', data)
    

class ApprovalStatusChange(View):
    def get(self, request,log_pk, status):
        task=TaskLog.objects.get(id=log_pk)
        task.result_status=status
        task.save()
        if status == 'Approved':
            ToDo.objects.filter(id=task.task.id).update(name=task.name,
                                                        description=task.description,
                                                        category=task.category,
                                                        status=task.status,
                                                        due_date=task.due_date)
        else:
            pass
        return HttpResponseRedirect(request.META['HTTP_REFERER'])