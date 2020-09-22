from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return render(request, "homepage.html")

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

