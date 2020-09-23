from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('add_project/<int:class_id>', views.add_project),
    path('add_student/<int:class_id>', views.add_student),
    path('class/<int:class_id>', views.class_render),
    path('request_appointment', views.calendar),
    path('register', views.register),
    path('add_user', views.add_user),
    path('login', views.login),
    path('log_in', views.log_in),
    path('success', views.success),
    path('logout', views.logout),
    path('user_info',views.user),
    path('edit_class/<int:class_id>', views.edit_class),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)