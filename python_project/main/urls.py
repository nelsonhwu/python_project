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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)