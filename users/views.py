from binascii import rledecode_hqx
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.urls import conf
from django.db.models import Q
from .models import Profile, Message, Opportunity
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm, SocialForm, OpportunityForm
from .utils import searchProfiles, paginateProfiles, searchAffiliates, paginateAffiliates, searchOpportunities
from datetime import datetime, timedelta


def loginUser(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request, 'Username OR password is incorrect')
    
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            
            group = Group.objects.get(name='Authenticated') 
            group.user_set.add(user)
            
            messages.success(request, 'User account was created!')
            
            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.success(
                request, 'An error has occurred during registration')
    
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query,
                'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, slug):
    profile = Profile.objects.get(slug = slug)
    
    topSkills = profile.skill_set.exclude(description__exact = "")
    otherSkills = profile.skill_set.filter(description = "")
    social = profile.social_set.all()
    
    context = {'profile': profile, 'topSkills': topSkills,
                'otherSkills': otherSkills, 'social': social}
    return render(request, 'users/user-profile.html', context)


def affiliates(request):
    profiles, search_query = searchAffiliates(request)

    custom_range, profiles = paginateAffiliates(request, profiles, 3)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request=request, template_name="users/affiliates.html", context=context)


def affiliateProfile(request, slug):
    profile = Profile.objects.get(slug = slug)
    context = {'profile': profile};
    return render(request=request, template_name="users/affiliate-profile.html", context=context)


@login_required(login_url = 'login')
def userAccount(request):
    profile = request.user.profile
    
    skills = profile.skill_set.all()
    social = profile.social_set.all()
    projects = profile.project_set.all()
    
    context = {'profile': profile, 'skills': skills, 'projects': projects, 'social': social}
    return render(request, 'users/account.html', context)


@login_required(login_url = 'login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)
    
    if profile.profile_type == 'alum':
        del form.fields['organization_name']
    else:
        del form.fields['short_intro']
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, profile)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            location = form.cleaned_data['location']
            profile_type = form.cleaned_data['profile_type']
            bio = form.cleaned_data['bio']
            
            if profile.profile_type == 'alum':
                short_intro = form.cleaned_data['short_intro']
            else:
                organization_name = form.cleaned_data['organization_name']
            profile_set = Profile.objects.filter(id = profile.id)
            profile_set.update(name = name, username = username, email = email, bio = bio, location = location, profile_type = profile_type)
            
            if profile.profile_type == 'alum':
                profile_set.update(short_intro = short_intro)
            else:
                profile_set.update(organization_name = organization_name)
            
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


#--------Skills--------


@login_required(login_url = 'login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit = False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url = 'login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    form = SkillForm(instance = skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url = 'login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    
    context = {'object': skill}
    return render(request, 'delete_template.html', context)


#----------Social----------


@login_required(login_url = 'login')
def createSocial(request):
    profile = request.user.profile
    form = SocialForm()
    
    if request.method == 'POST':
        form = SocialForm(request.POST)
        if form.is_valid():
            social = form.save(commit = False)
            social.owner = profile
            social.save()
            messages.success(request, 'Site was added successfully!')
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/social_form.html', context)


@login_required(login_url = 'login')
def updateSocial(request, pk):
    profile = request.user.profile
    social = profile.social_set.get(id = pk)
    form = SocialForm(instance = social)
    
    if request.method == 'POST':
        form = SocialForm(request.POST, instance = social)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site was updated successfully!')
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/social_form.html', context)


@login_required(login_url = 'login')
def deleteSocial(request, pk):
    profile = request.user.profile
    social = profile.social_set.get(id = pk)
    if request.method == 'POST':
        social.delete()
        messages.success(request, 'Site was deleted successfully!')
        return redirect('account')
    
    context = {'object': social}
    return render(request, 'delete_template.html', context)


#--------Messages----------


@login_required(login_url = 'login')
def inbox(request, slug):
    profile = Profile.objects.get(slug = slug)
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read = False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    
    return render(request, 'users/inbox.html', context)


@login_required(login_url = 'login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id = pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, slug):
    recipient = Profile.objects.get(slug = slug)
    form = MessageForm()
    
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit = False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', slug = recipient.slug)
    
    context = {'recipient': recipient, 'sender': sender, 'form': form}
    return render(request, 'users/message_form.html', context)


@login_required(login_url = 'login')
def replyMessage(request, slug):
    recipient = Profile.objects.get(slug = slug)
    form = MessageForm()
    
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit = False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            
            messages.success(request, 'Your message was successfully sent!')
            return redirect('inbox', slug = sender.slug)
    
    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


@login_required(login_url = 'login')
def deleteMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id = pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message was deleted successfully!')
        return redirect('inbox', profile.slug)
    
    context = {'object': message}
    return render(request, 'delete_template.html', context)


#--------Opportunities----------


# @login_required(login_url = 'login')
def opportunityBoard(request):
    # automatically deletes opportunities more than 90 days old
    Opportunity.objects.filter(created__lte = datetime.now()-timedelta(days=90)).delete()
    
    opportunities, search_query = searchOpportunities(request)
    
    if request.user.is_authenticated:        
        profile = request.user.profile
        read = profile.read.all()
    else:
        read = None
    
    context = {
                'opportunities': opportunities,
                'search_query': search_query, 
                'read': read,
            }
    
    return render(request, 'users/opportunity_board.html', context)


# @login_required(login_url = 'login')
def viewOpportunity(request, pk):
    opportunity = Opportunity.objects.get(id=pk)
    
    if request.user.is_authenticated:
        profile = request.user.profile    
        if opportunity not in profile.read.all():
            profile.read.add(opportunity)
        
        # opportunity.save()
    context = {'opportunity': opportunity}
    
    return render(request, 'users/opportunity.html', context)


def createOpportunity(request):
    form = OpportunityForm()
    
    try:
        creator = request.user.profile
    except:
        creator = None
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            
            opportunity = form.save(commit = False)
            opportunity.owner = creator
            
            if creator:
                opportunity.poster = creator.name
            
            opportunity.save()
            
            messages.success(request, 'Your opportunity was successfully posted!')
            return redirect('opportunity-board')
    
    context = {'form': form} 
    return render(request, 'users/opportunity_form.html', context)


def updateOpportunity(request, pk):
    post = Opportunity.objects.get(pk = pk)
    form = OpportunityForm(instance = post)
    
    try:
        creator = request.user.profile
    except:
        creator = None
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance = post)
        if form.is_valid():
            
            opportunity = form.save(commit = False)
            opportunity.owner = creator
            
            if creator:
                opportunity.poster = creator.name
            
            opportunity.save()
            
            messages.success(request, 'Your opportunity was successfully posted!')
            context = {'opportunity': post}
            return redirect('opportunity-board')
    
    context = {'form': form}
    return render(request, 'users/opportunity_form.html', context)


# if user is logged in and they are the creator of an opportunity post,
# allow them to delete it
@login_required(login_url = 'login')
def deleteOpportunity(request, pk):
    profile = request.user.profile
    opportunity = Opportunity.objects.get(id = pk)
    if request.method == 'POST':
        opportunity.delete()
        messages.success(request, 'Opportunity post was deleted successfully!')
        return redirect('opportunity-board')
    
    context = {'object': opportunity}
    return render(request, 'delete_template.html', context)