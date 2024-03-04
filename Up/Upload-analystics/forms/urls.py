from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.fileUpload, name='fileUpload'),
    path('replace_filename/', views.replace_filename, name='replace_filename'),
    # path('filesList/', views.filesList, name = 'filesList'),
    path('getColumnList/', views.getColumnList, name = 'getColumnList'),
    path('list_datasources/', views.list_datasources, name='list_datasources'),
    path('list_files/', views.list_files, name='list_files'),
    path('CreateDataFrame/',views.CreateDataFrame,name='CreateDataFrame'),
]