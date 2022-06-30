from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name = "projects"),
    path('project/<str:owner>/<str:slug>/', views.project, name = "project"),
    
    path('project/<str:owner>/<str:slug>/demo-conf', views.projectDemoConf, name = "demo-conf"),

    path('project/', views.createProject, name = "create-project"),

    path('project/<str:owner>/<str:slug>/update/', views.updateProject, name = "update-project"),

    path('project/<str:owner>/<str:slug>/delete/', views.deleteProject, name = "delete-project"),
]
