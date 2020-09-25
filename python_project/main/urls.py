from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
####################################################################
    path('add_relation', views.add_relation),
    path('class/<int:class_id>/edit', views.edit_class),
    path('class/new', views.new_class),
    path('class/create', views.create_class),
    path('edit_class/<int:class_id>', views.edit_class_post),
    path('image/all', views.image_block),
    path('image/<int:image_id>', views.image_viewer),
    path('image/<int:image_id>/add_message', views.add_message),
    path('image/<int:image_id>/add_comment', views.add_comment),
    path('image/<int:image_id>/delete/<int:message_id>', views.delete_message),
    path('about_us', views.about_us),
    path('class_info', views.all_class),
    path('bulletin/add_bulletin', views.add_bulletin),
    path('bulletin/<int:bulletin_id>/delete', views.delete_bulletin),


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
    # path('success', views.success),
    path('logout', views.logout),
    path('user_info',views.user),
    path('user_homepage', views.user_homepage),

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