from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import timedelta
from .models import Task
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from accounts.models import User

# Create your views here.



def search(request):
    search_query=request.GET.get('search')
    tasks=Task.objects.filter(Q(title__icontains=search_query) | 
            Q(description__icontains=search_query))
    t=[]
    for task in tasks:
        if task.completed==False and task.user==request.user:
            t.append(task)
    print(search_query)
    return render(request,'searchedTask.html',{'tasks':t,'search_query':search_query})
  
@login_required(login_url= 'login')  
def show_tasks(request):
    users=User.objects.all()
    now=timezone.now()
    new_time = now + timedelta(hours=5, minutes=30)
    today = new_time.date()
    tomorrow = today + timedelta(days=1) 
    if request.method=='POST':
        task_title = request.POST.get('taskTitle')
        task_description = request.POST.get('taskDescription')
        task_time = request.POST.get('taskTime')
        task_date = request.POST.get('taskDate')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        assigned_to=request.POST.get('assigned_to')
        u=User.objects.get(id=assigned_to)
        Task.objects.create(
            title=task_title,
            description=task_description,
            due_time=task_time,
            due_date=task_date,
            priority=priority,
            category=category,
            assigned_to=u,
            user=request.user
        )
    overdue_tasks=Task.objects.filter(completed=False,due_date__lt=today,user=request.user)
    today_overdue_tasks=Task.objects.filter(completed=False,due_date=today,due_time__lt=new_time,user=request.user)
    today_tasks = Task.objects.filter(completed=False,due_date=today,due_time__gt=new_time,user=request.user)  
    tomorrow_tasks = Task.objects.filter(completed=False,due_date=tomorrow,user=request.user)
    upcoming_tasks=Task.objects.filter(completed=False,due_date__gt=tomorrow,user=request.user)
    context = {
        'users':users,
            'current_date':today,
            'next_date':tomorrow,
            'overdue_tasks':overdue_tasks,
            'today_overdue_tasks':today_overdue_tasks,
            'today_tasks': today_tasks,
            'tomorrow_tasks': tomorrow_tasks,
            'upcoming_tasks':upcoming_tasks
        }
    return render(request, 'tasks.html', context)


def edit_task(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method=='POST':
        task.title = request.POST.get('taskTitle')
        task.description = request.POST.get('taskDescription')
        task.due_time = request.POST.get('taskTime')
        task.due_date = request.POST.get('taskDate')
        task.priority = request.POST.get('priority')
        task.category = request.POST.get('category')
        task.save()
        return redirect('showTasks')
    return render(request,'editTask.html',{'task': task})

def delete_task(request,task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('showTasks')
    
    
def complete_task(request, task_id):
    task=Task.objects.get(id=task_id)
    task.completed=True
    task.save()
    return redirect('showTasks')

def filter_tasks(request,category):
    tasks=Task.objects.filter(completed=False,category=category,user=request.user)
    return render(request,'filteredTask.html',{'tasks': tasks,'Category':category})
