from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.fileUpload, name='fileUpload'),
    path('replace_filename/', views.replace_filename, name='replace_filename'),
    path('filesList/', views.filesList, name = 'filesList'),
    path('getColumnList/', views.getColumnList, name = 'getColumnList'),
]