from django.shortcuts import render, HttpResponse, redirect
from .models import User, Class, Project, Message, Comment

def index(request):
    return HttpResponse("Python Project Basics Are Functioning")

def add_project(request, class_id):
    current_class = Class.objects.get(id=class_id)
    title = request.POST['title']
    due_date = request.POST['due_date']
    desc = request.POST['desc']
    new_project = Project.objects.create(
        title = title, 
        due_date = due_date, 
        desc = desc
    )
    current_class.project_classes.add(new_project)
    return redirect(f'/class/{class_id}')

def add_student(request, class_id):
    current_class = Class.objects.get(id=class_id)
    new_student_id = request.POST['student.id']
    new_student = User.objects.get(id=new_student_id)
    current_class.parent_classes.add(new_student)
    return redirect(f'/class/{class_id}')

def class_render(request, class_id):
    logged_in_user = User.obejcts.get(id=request.session['user_id'])
    context={
        this_class : Class.objects.get(id=class_id),
        user : logged_in_user
    }
    return render(request, 'class.html', context)

def calendar(request):
    return render(request, 'calendar.html')
