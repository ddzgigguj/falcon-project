from django.urls import path
from . import views

urlpatterns = [
path('submit/', views.submit_application, name='submit_application'),
path('my-applications/', views.user_applications, name='user_applications'),
path('detail/<int:app_id>/', views.application_detail, name='application_detail'),
path('admin/', views.admin_applications, name='admin_applications'),
path('admin/<int:app_id>/', views.admin_application_detail, name='admin_application_detail'),
path('admin/<int:app_id>/download/', views.download_application_files, name='download_application_files'),
]