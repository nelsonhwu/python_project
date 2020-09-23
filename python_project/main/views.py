from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Class, Project, Message, Comment, Image
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
        'user' : logged_in_user
    }
    return render(request, 'class.html', context)

def new_class(request):
    return render(request, 'new_class.html')

def create_class(request):
    errors = User.objects.class_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/class/new')
    else:
        subject = request.POST['subject']
        start_date = request.POST['start_date']
        end_date = request.POST['start_date']
        schedule_day = request.POST['schedule_day']
        schedule_time = request.POST['schedule_time']
        desc = request.POST['desc']
        new_class = Class.objects.create(
            subject = subject,
            start_date = start_date,
            end_date = end_date,
            schedule_day = schedule_day,
            schedule_time = schedule_time,
            desc = desc
        )
        return redirect(f'/class/{new_class.id}')


def edit_class(request, class_id):
    context={
        'user': User.objects.get(id=request.session['user_id']),
        'this_class' : Class.objects.get(id=class_id)
    }
    return render(request, 'edit_class.html', context)

def edit_class_post(request, class_id):
    errors = User.objects.update_class_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/edit_class/{class_id}')
    else:
        subject = request.POST['subject']
        start_date = request.POST['start_date']
        end_date = request.POST['start_date']
        schedule_day = request.POST['schedule_day']
        schedule_time = request.POST['schedule_time']
        desc = request.POST['desc']
        current_class = Class.objects.get(id=class_id)
        if subject:
            current_class.subject = subject
            current_class.save()
        if start_date:
            current_class.start_date = start_date
            current_class.save()
        if end_date:
            current_class.end_date = end_date
            current_class.save()
        if not schedule_day == 'none':
            current_class.schedule_day = schedule_day
            current_class.save()
        if schedule_time:
            current_class.schedule_time = schedule_time
            current_class.save()
        if desc:
            current_class.desc = desc
            current_class.save()
        return redirect(f'/class/{class_id}')


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
    errors = User.objects.login_validation(request.POST)
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
    print(logged_in_user.__dict__)
    context = {
        'logged_in_user' : logged_in_user,
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def user(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_in_user':logged_in_user,
    }
    return render(request, 'user_info.html',context)

def image_block(request):
    context = {
        'all_images': Image.objects.all()
    }
    return render(request, 'image.html', context)

def image_viewer(request, image_id):
    current_image = Image.objects.get(id=image_id)
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context={
        'this_image':current_image,
        'user': logged_in_user,
        'all_messages': Message.objects.all(),
        'all_comments': Comment.objects.all(),
    }
    return render(request, 'viewer.html', context)

def add_message(request, image_id):
    message = request.POST['message']
    Message.objects.create(message = message, user_id = User.objects.get(id=request.session['user_id']))
    return redirect(f'/image/{image_id}')

def add_comment(request, image_id):
    comment = request.POST['comment']
    user = User.objects.get(id=request.session['user_id'])
    message_id = request.POST['message_id']
    Comment.objects.create(comment = comment, message_id=Message.objects.get(id= message_id), user_id = user)
    return redirect(f'/image/{image_id}')

def delete_message(request, image_id, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()
    return redirect(f'/image/{image_id}')