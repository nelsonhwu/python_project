from django.shortcuts import render, HttpResponse, redirect
from .models import User, Class, Project, Message, Comment, Image
import bcrypt
from datetime import date, datetime, timezone
from django.contrib import messages
from .forms import IamgeForm

##########################################################################################################
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
        "this_class" : Class.objects.get(id=class_id),
        "user" : logged_in_user
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
            return redirect('/user_info')
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








##########################################################################################################

def edit_account(request, user_id):
    if "user_id" in request.session:

        logged_user = User.objects.get(id=user_id)

        return render(request, "accountEdit.html", {"logged_user": logged_user})
    return redirect("/")

def update (post_field, user_id):
    logged_user = User.objects.get(id=user_id)
    if post_field == "profile_image":
        profile_image = request.FILES["profile_image"]
        logged_user.profile_image.save(profile_image.name, profile_image)
        logged_user.save()
        return logged_user
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
        errors = User.objects.edit_account_validation(request.POST)

        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value, extra_tags="edit_err")
            return redirect("/edit_account")
        else:
            for key in request.POST.keys():
                updated_user = updata(key, user_id)
                updated_user.save()
            success_message = "Profile updated successfully!"
            messages.success(request, success_message)
            return redirect("/edit_account")

def project_detail(request, project_id):
    if "user_id" in request.session:

        logged_user = User.objects.get(id=request.session["user_id"])
        cur_proj = Project.objects.get(id=project_id)
        total_images = len(cur_proj.images.all())

        form = ImageForm()
        form.fields["submission"].initial = request.logged_user.id
        form.fields["submitter"].initial = request.cur_proj.id

        context = {
            "logged_user": logged_user,
            "cur_proj": cur_proj,
            "total_images": total_images,
            "form": form,
        }

        return render(request, "projectDetail.html", context)
    return redirect("/")

def process_upload(request, project_id):
    logged_user = User.objects.get(id=request.session["user_id"])
    cur_proj = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            return redirect(f'/project_detail/{cur_proj.id}')
        else:
            form = ImageForm()
            error="Must have a title and an uploaded file!"
            messages.error(request, error, extra_tags="upload_err")
            context = {
                "form" : form,
            }
            return render(request, 'projectDetail.html', context) 


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
            "cur_proj": cur_proj,
            "all_classes": all_classes,
        }
        return render(request, "projectEdit_html", context)
    return redirect("/")


        
def update_proj_func(post_field, cur_proj):
    if len(request.POST[post_field]) !=0:
        cur_proj[post_field] = request.POST[post_field]
        cur_proj.save()
        return cur_proj

def process_edit_project(request, project_id):
    logged_user = User.objects.get(id=request.session["user_id"])
    cur_proj = Project.objects.get(id=project_id)
    errors = Project.objects.edit_project_validation(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value, extra_tags="edit_proj_err")
        return redirect(f"/edit_project/{cur_proj.id}")
    else:
        for key in request.POST.keys():
            cur_proj = update_proj_func(key, cur_proj)
            cur_proj.save()
        success_message = "Profile updated successfully!"
        messages.success(request, success_message)
        return redirect(f"/edit_project/{cur_proj.id}")
        

