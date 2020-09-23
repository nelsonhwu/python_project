from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('add_user', views.add_user),
    path('login', views.login),
    path('log_in', views.log_in),
    path('success', views.success),
    path('logout', views.logout),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)