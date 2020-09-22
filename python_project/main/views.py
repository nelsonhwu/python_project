from django.shortcuts import render, HttpResponse, redirect
from .models import User,Class,Project,Message,Comment,Image

def index(request):
    return HttpResponse("Python Project Basics Are Functioning")


def user(request):
    logged_in_user = User.objects.get(id=request.session['user_id']
        context={
        'logged_in_user':logged_in_user,
    }
    return render(request, 'user_info.html',context)