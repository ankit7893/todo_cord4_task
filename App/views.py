from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from . models import *
from . forms import *

# Create your views here.

class TodoList(View):
    def get(self, request):
        list = ToDo.objects.filter(user=request.user)
        shared_tasks = TodoShareModal.objects.filter(user=request.user)
        data = {
            'todolist':list,
            'todoform':TodoForm(),
            'users':User.objects.all(),
            'shared_tasks':shared_tasks
            }
        return render(request, 'app/ViewList.html', data)

    def post(self, request):
        form = TodoForm(request.POST)
        if form.is_valid():
            form=form.save(commit=True)
            form.user=request.user
            form.save()
            print("Done")
        else:
            print("not done")    
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class TodoListDelete(View):
    def get(self, request,pk):
        list = ToDo.objects.get(id=pk)
        list.delete()
        return redirect('/list')


class TodoListEdit(View):
    def get(self, request, pk):
        list = ToDo.objects.get(id=pk)
        form = TodoForm(instance = list)
        data = {
            'todoform':form
            }
        return render(request, 'app/EditList.html', data)

    def post(self, request, pk):
        list = ToDo.objects.get(id=pk)
        form = TodoForm(request.POST, instance=list)
        if form.is_valid():
            form.save()
            print("Done")
        else:
            print("not done")    
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class TodoListShare(View):
    def post(self, request, pk):
        print(pk)
        task = ToDo.objects.get(id=pk)
        user = User.objects.get(id=int(request.POST['user']))  
        share_permission = TodoShareModal.objects.create(task=task, user=user, permission=request.POST['permission']) 
        return redirect('/list')


