from django.shortcuts import render, HttpResponse, redirect
from .models import User, Class, Project, Message, Comment, Image, Relationship
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "homepage.html")

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
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context={
        'this_class' : Class.objects.get(id=class_id),
        user : logged_in_user
    }
    return render(request, 'class.html', context)

def calendar(request):
    return render(request, 'calendar.html')
def register(request):
    return render(request, "register.html")

def add_user(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/register')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
        street_address = request.POST['street_address'],
        city = request.POST['city'],
        state = request.POST['state'],
        zip_code = request.POST['zip_code'],
        phone = request.POST['phone'],
        access_level = request.POST['access_level']
    )
    request.session['user_id'] = new_user.id
    return redirect('/success')

def login(request):
    return render(request, "login.html")

def log_in(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/login')
    list_of_users = User.objects.filter(email=request.POST['email'])
    if len(list_of_users) > 0:
        user = list_of_users[0]
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), user.password.encode()):
            request.session['user_id'] = user.id
        return redirect('/success')
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    all_relationships = Relationship.objects.all()
    context = {
        'logged_in_user' : logged_in_user,
        'all_relationships' : all_relationships
    }
    return render(request, "success.html", context)

def add_relation(request):
    if 'user_id' not in request.session:
        return('/')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    errors = User.objects.related_person_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect("/success")        
    list_of_users = User.objects.filter(email=request.POST['email'])
    print("Working Here1")
    if len(list_of_users) > 0:
        person_to_add = list_of_users[0]
        print("%"*60)
        print(person_to_add)
        Relationship.objects.create(
            from_user=logged_in_user,
            to_user=person_to_add,
            status=request.POST['status']
        )
        return redirect("/success")
    else:
        return redirect("/success")

def logout(request):
    request.session.clear()
    return redirect('/')

def user(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_in_user':logged_in_user,
    }
    return render(request, 'user_info.html',context)

def index2(request):
    all_users = User.objects.all()
    context = {
        'all_users' : all_users
    }
    return render(request, "index.html", context)
