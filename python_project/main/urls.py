from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
####################################################################

    path('class/<int:class_id>/edit', views.edit_class),
    path('class/new', views.new_class),
    path('class/create', views.create_class),
    path('edit_class/<int:class_id>', views.edit_class_post),
    path('image/all', views.image_block),
    path('image/<int:image_id>', views.image_viewer),
    path('image/<int:image_id>/add_message', views.add_message),
    path('image/<int:image_id>/add_comment', views.add_comment),
    path('image/<int:image_id>/delete/<int:message_id>', views.delete_message),


####################################################################

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
<<<<<<< HEAD
<<<<<<< HEAD
    path('user_info',views.user),
    path('add_relation', views.add_relation),
<<<<<<< HEAD
=======
    path('index', views.index2),
=======
    path('user_info',views.user)
>>>>>>> parent of f98ce8c... 09/23/2020

    path('class/<int:class_id>/edit', views.edit_class),
    path('class/new', views.new_class),
    path('class/create', views.create_class),
    path('edit_class/<int:class_id>', views.edit_class_post),
    path('image/all', views.image_block),
    path('image/<int:image_id>', views.image_viewer),
    path('image/<int:image_id>/add_message', views.add_message),
    path('image/<int:image_id>/add_comment', views.add_comment),
    path('image/<int:image_id>/delete/<int:message_id>', views.delete_message),
=======
    path('user_info',views.user)
>>>>>>> parent of f98ce8c... 09/23/2020

<<<<<<< HEAD
>>>>>>> parent of 6745074... 09/24/2020
=======
>>>>>>> parent of 6745074... 09/24/2020

####################################################################
    path('project_detail/<int:project_id>', views.project_detail),
    path('process_upload/<int:project_id>', views.process_upload),
    path('edit_account/<int:user_id>', views.edit_account),
    path('process_edit_user/<int:user_id>', views.process_edit_user),
    path('edit_project/<int:project_id>', views.edit_project),
    path('process_edit_project/<int:project_id>', views.process_edit_project),
    path('process_reviewed/<int:project_id>', views.process_reviewed),
    path('process_unreviewed/<int:project_id>', views.process_unreviewed),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)