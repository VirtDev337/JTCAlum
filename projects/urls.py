from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name = "projects"),
    path('project/<str:slug>/', views.project, name = "project"),

    path('project/', views.createProject, name = "create-project"),

    path('project/<str:slug>/update/', views.updateProject, name = "update-project"),

    path('project/<str:slug>/delete/', views.deleteProject, name = "delete-project"),
]
