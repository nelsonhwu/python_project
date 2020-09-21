from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return HttpResponse("Python Project Basics Are Functioning")


