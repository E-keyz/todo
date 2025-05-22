from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from itertools import groupby
from django.utils.timezone import localtime
from django.db.models.functions import TruncDate

from tasks.models import Task

# Create your views here.

from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check for duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('task_list')

    return render(request, 'tasks/register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'tasks/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def task_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        if title and priority:
            Task.objects.create(title=title, priority=priority, user=request.user)
            return redirect('/')
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('/')

@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    
    return render(request, 'tasks/confirm_delete.html', {'task': task})




@login_required(login_url='login')
def dashboard(request):
    tasks = (
        Task.objects
        .annotate(created_date=TruncDate('created_at'))
        .order_by('-created_date')
    )

    grouped_tasks = {}
    for date, items in groupby(tasks, key=lambda x: x.created_date): # type: ignore
        grouped_tasks[date] = list(items)

    #total = tasks.count()
   # completed = tasks.filter(completed=True).count()
    #pending = total - completed
    

    return render(request, 'tasks/dashboard.html', {
        'grouped_tasks': grouped_tasks,
        #'total': total,
       # 'completed': completed,
        #'pending': pending,
    
    })


   # total = tasks.count()
    #completed = tasks.filter(completed=True).count()
   # pending = total - completed
   # recent_tasks = tasks.order_by('id')[:5]

   # context = {
    #    'user': user,
   #     'total': total,
   #     'completed': completed,
   #     'pending': pending,
    #    'recent_tasks': recent_tasks,
   # }

    #return render(request, 'tasks/dashboard.html', {'grouped_tasks': grouped_tasks})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        completed = request.POST.get('completed') == 'on'
        if title:
            task.title = title
            task.completed = completed
            task.priority = priority
            task.save()
            return redirect('dashboard')
        
    return render(request, 'tasks/edit_task.html', {'task': task})

def toggle_complete(request, task_id):
     task = get_object_or_404(Task, id=task_id)
     task.completed = not task.completed
     task.save()
     return redirect('dashboard')
