from django.shortcuts import render, HttpResponse, redirect
from .models import User, Class, Project, Message, Comment
from .models import User, Class, Project, Message, Comment, Image
from django.contrib import messages
import bcrypt
from .models import User,Class,Project,Message,Comment,Image

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
    logged_in_user = User.obejcts.get(id=request.session['user_id'])
    context={
<<<<<<< HEAD
        'this_class' : Class.objects.get(id=class_id),
        'user' : logged_in_user
=======
        this_class : Class.objects.get(id=class_id),
        user : logged_in_user
>>>>>>> parent of f98ce8c... 09/23/2020
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

def image_block(request):
    context = {
        'all_images': Image.objects.all()
    }
    return render(request, 'images.html', context)

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
    
def user(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_in_user':logged_in_user,
    }
    return render(request, 'user_info.html',context)

def edit_account(request, user_id):
    if "user_id" in request.session:

        logged_user = User.objects.get(id=user_id)

        return render(request, "accountEdit.html", {"logged_user": logged_user})
    return redirect("/")

def update (post_field, user_id):
    
    if len(request.POST[post_field]) !=0 and post_field != "password":
        logged_user[post_field] = request.POST[post_field]
        logged_user.save()
        return logged_user

    elif len(request.POST[post_field]) !=0 and post_field == "password":
        pw = request.POST[post_field]
        pw_hash = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode()
        logged_user[post_field] = pw_hash
        logged_user.save()
        return logged_user

def process_edit_user(request, user_id):
        user_id = user_id
        logged_user = User.objects.get(id=user_id)
        errors = User.objects.edit_account_validation(request.POST)

        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value, extra_tags="edit_err")
            return redirect(f"/edit_account/{user_id}")
        else:
            if "profile_image" in request.FILES:
                profile_image = request.FILES["profile_image"]
                logged_user.profile_image.save(profile_image.name, profile_image)
                logged_user.save()
            if len(request.POST["password"]) !=0:
                pw = request.POST[post_field]
                pw_hash = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode()
                logged_user.password = pw_hash
                logged_user.save()
            if len(request.POST["first_name"]) !=0:
                logged_user.first_name = request.POST["first_name"]
                logged_user.save()
            if len(request.POST["last_name"]) !=0:
                logged_user.last_name = request.POST["last_name"]
                logged_user.save()
            if len(request.POST["email"]) !=0:
                logged_user.email = request.POST["email"]
                logged_user.save()
            if len(request.POST["street_address"]) !=0:
                logged_user.street_address = request.POST["street_address"]
                logged_user.save()
            if len(request.POST["city"]) !=0:
                logged_user.city = request.POST["city"]
                logged_user.save()
            if len(request.POST["state"]) !=0:
                logged_user.state = request.POST["state"]
                logged_user.save()
            if len(request.POST["zip_code"]) !=0:
                logged_user.zip_code = request.POST["zip_code"]
                logged_user.save()
            if len(request.POST["phone"]) !=0:
                logged_user.phone = request.POST["phone"]
                logged_user.save()
            success_message = "Profile updated successfully!"
            messages.success(request, success_message)
            return redirect(f"/edit_account/{logged_user.id}")

def project_detail(request, project_id):
    if "user_id" in request.session:

        logged_user = User.objects.get(id=request.session["user_id"])
        cur_proj = Project.objects.get(id=project_id)
        total_images = len(cur_proj.images.all())

        context = {
            "logged_user": logged_user,
            "cur_proj": cur_proj,
            "total_images": total_images,
        }

        return render(request, "projectDetail.html", context)
    return redirect("/")

def process_upload(request, project_id):
    logged_user = User.objects.get(id=request.session["user_id"])
    cur_proj = Project.objects.get(id=project_id)

    errors = Project.objects.upload_image_validation(request.POST)
    if len(request.FILES["picture"]) ==0:
        errors["picture"] = "You must include you work to submit!"
    if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value, extra_tags="upload_img_err")
            return redirect(f"/process_upload/{cur_proj.id}")
    else:
        title = request.POST["title"]
        image = request.FILES["picture"]
        new_image = Image()
        new_image.title = title
        new_image.submission = cur_proj
        new_image.submitter = logged_user
        new_image.save()
        new_image.picture.save(image.name, image)

        return redirect("/image/all")


def process_reviewed(request, project_id):
    logged_user = User.objects.get(id=request.session["user_id"])
    cur_proj = Project.objects.get(id=project_id)
    cur_proj.reviewed_by_user.add(logged_user)
    cur_proj.save()
    return redirect(f'/project_detail/{cur_proj.id}')

def process_unreviewed(request, project_id):
    logged_user = User.objects.get(id=request.session["user_id"])
    cur_proj = Project.objects.get(id=project_id)
    cur_proj.reviewed_by_user.remove(logged_user)
    cur_proj.save()
    return redirect(f'/project_detail/{cur_proj.id}')


def edit_project(request, project_id):
    if "user_id" in request.session:

        logged_user = User.objects.get(id=request.session["user_id"])
        cur_proj = Project.objects.get(id=project_id)
        all_classes = Class.objects.all()
        context = {
            "logged_user": logged_user,
            "cur_proj": cur_proj,
            "all_classes": all_classes,
        }
        return render(request, "projectEdit.html", context)
    return redirect("/")

def process_edit_project(request, project_id):
    logged_user = User.objects.get(id=request.session["user_id"])
    cur_proj = Project.objects.get(id=project_id)
    errors = Project.objects.edit_project_validation(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value, extra_tags="edit_proj_err")
        return redirect(f"/edit_project/{cur_proj.id}")
    else:
        if len(request.POST["title"]) !=0:
            cur_proj.title = request.POST["title"]
            # cur_proj.save()
        if len(request.POST["due_date"]) !=0:
            cur_proj.due_date = request.POST["due_date"]
            # cur_proj.save()
        if len(request.POST["desc"]) !=0:
            cur_proj.desc = request.POST["desc"]
        if len(request.POST["course"]) !=0:
            course = Class.objects.get(id=request.POST["course"])
            cur_proj.course = course
        cur_proj.save()
        success_message = "Project updated successfully!"
        messages.success(request, success_message)
        return redirect(f"/edit_project/{cur_proj.id}")

def calendar(request):
    return render(request, 'calendar.html')

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

<<<<<<< HEAD
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

    print(logged_in_user.__dict__)
=======
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
>>>>>>> parent of f98ce8c... 09/23/2020
    context = {
        'logged_in_user' : logged_in_user,
    }
<<<<<<< HEAD
    return render(request, "success.html", context)

def index2(request):
    all_users = User.objects.all()
    context = {
        'all_users' : all_users
    }
    return render(request, "index.html", context)
=======
    return render(request, 'user_info.html',context)
>>>>>>> parent of f98ce8c... 09/23/2020
