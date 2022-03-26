from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerUser, name = "register"),

    path('', views.profiles, name = "profiles"),
    path('profile/<str:slug>/<str:pk>/', views.userProfile, name = "user-profile"),
    path('account/', views.userAccount, name = "account"),

    path('account/update', views.editAccount, name = "edit-account"),

    path('create-skill/', views.createSkill, name = "create-skill"),
    path('update-skill/<str:pk>/', views.updateSkill, name = "update-skill"),
    path('delete-skill/<str:pk>/', views.deleteSkill, name = "delete-skill"),
    
    path('create-site/', views.createSocial, name = "create-site"),
    path('update-site/<str:pk>/', views.updateSocial, name = "update-site"),
    path('delete-site/<str:pk>/', views.deleteSocial, name = "delete-site"),
    
    path('inbox/', views.inbox, name = "inbox"),
    path('message/<str:pk>/', views.viewMessage, name = "message"),
    path('create-message/<str:pk>/', views.createMessage, name = "create-message"),
]
