from django.urls import path, include
# from .forms import CustomAuthForm
from . import views

urlpatterns = [
    path('login/', views.loginUser, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerUser, name = "register"),
    
    path('', views.profiles, name = "profiles"),
    path('profile/<str:slug>/', views.userProfile, name = "user-profile"),
    path('account/', views.userAccount, name = "account"),
    path('account/update', views.editAccount, name = "edit-account"),
    
    path('affiliates/', views.affiliates, name='affiliates'),
    path('affiliate/profile/<str:slug>/', views.affiliateProfile, name='affiliate-profile'),


    path('skill/create/', views.createSkill, name = "create-skill"),
    path('skill/update/<str:pk>/', views.updateSkill, name = "update-skill"),
    path('skill/delete/<str:pk>/', views.deleteSkill, name = "delete-skill"),
    
    path('site/create/', views.createSocial, name = "create-site"),
    path('site/update/<str:pk>/', views.updateSocial, name = "update-site"),
    path('site/delete/<str:pk>/', views.deleteSocial, name = "delete-site"),
    
    path('<str:slug>/inbox/', views.inbox, name = "inbox"),
    path('message/<str:pk>/', views.viewMessage, name = "message"),
    path('message/create/<str:slug>/', views.createMessage, name = "create-message"),
    path('message/reply/<str:slug>/', views.replyMessage, name = "reply-message"),
    path('message/delete/<str:pk>/', views.deleteMessage, name = "delete-message"),

    path('opportunities/', views.opportunityBoard, name = "opportunity-board"),
    path('opportunity/create/', views.createOpportunity, name = "create-opportunity"),
    path('opportunity/<str:pk>/', views.viewOpportunity, name = "opportunity"),
    path('opportunity/update/<str:pk>/', views.updateOpportunity, name = "update-opportunity"),
    path('opportunity/delete/<str:pk>/', views.deleteOpportunity, name = "delete-opportunity"),
]