from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

# View to display the list of tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# View to add a new task
def add_task(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST.get('description', '')
        Task.objects.create(title=title, description=description)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

# View to mark a task as completed
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

# View to delete a task
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

