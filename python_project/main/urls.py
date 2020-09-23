from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('project_detail/<int:project_id>', views.project_detail),
    path('process_upload/<int:project_id>', views.process_upload),
    path('edit_account/<int:user_id>', views.edit_account),
    path('process_edit_user/<int:user_id>', views.process_edit_user),
    path('edit_project/<int:project_id>', views.edit_project),
    path('process_edit_project/<int:project_id>', views.process_edit_project),
    path('process_reviewed/<int:project_id>', views.process_reviewed),
    path('process_unreviewed/<int:project_id>', views.process_unreviewed),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)