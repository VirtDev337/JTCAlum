from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm, DemoForm, SiteForm
from .utils import searchProjects, paginateProjects
# from jtcalumn.decorators import unread_count


# @unread_count()
def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


# @unread_count()
def project(request, owner, slug):
    projectObj = Project.objects.get(slug = slug)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit = False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', projectObj.owner, projectObj.slug)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})


@login_required(login_url = "login")
# @unread_count()
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name = tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url = "login")
# @unread_count()
def updateProject(request, owner, slug):
    profile = request.user.profile
    project = profile.project_set.get(slug = slug)
    form = ProjectForm(instance = project)
    
    if project.demo:
        del form.fields['demo_link']
    elif project.demo_link:
        del form.fields['demo']
    
    if request.method == 'POST':
        newtags = None
        
        try:
            newtags = request.POST.get('newtags').replace(',',  " ").split()
        except:
            pass
        
        form = ProjectForm(request.POST, request.FILES, instance = project)
        
        if form.is_valid():
            project = form.save()
            
            if newtags:
                for tag in newtags:
                    tag, created = Tag.objects.get_or_create(name = tag)
                    project.tags.add(tag)
            
            if project.demo and not project.demo_set:
                return redirect('demo-conf', project.owner, project.slug)
            
            if not project.demo and project.demo_set or project.site_name != '': 
                project.demo_set = False
                project.site_name = ""
                project.project_path = ""
                project.site_path = ""
                project.site.delete()
                Project.objects.filter(id = project.id).update(
                    demo_set = project.demo_set,  
                    site_name = project.site_name, 
                    project_directory = project.project_directory, 
                    site_path = project.site_path
                )
            
            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url = "login")
# @unread_count()
def projectDemoConf(request, owner, slug):
    profile = request.user.profile
    project = profile.project_set.get(slug = slug)
    dform = DemoForm(instance = project)
    sform = SiteForm(instance = project)
    
    if request.method == 'POST':
        dform = DemoForm(request.POST['dform'], request.FILES, instance = project)
        sform = DemoForm(request.POST['sform'], instance = project)
        
        if sform.is_valid():
            project.site = sform.save()['id']  
        
        if dform.is_valid():
            name = dform.cleaned_data['project_name']
            site_name = dform.cleaned_data['site_name']
            project_dir = dform.cleaned_data['project_path'] if dform.cleaned_data['project_path'] else name
            site_dir = dform.cleaned_data['site_path'] if dform.cleaned_data['site_path'] else site_name
            demo_set = project.demo_set
            
            if not demo_set:
                demo_set = True
            
            project_set = Project.objects.filter(id = project.id)
            project_set.update(
                project_name = name, 
                site_name = site_name, 
                project_directory = project_dir, 
                site_directory = site_dir
            )
            try:
                if not project_set.demo_set:
                    project_set.update(demo_set = demo_set)
            except:
                project_set.update(demo_set = demo_set)
            
            # if project.demo and project.demo_set:
            #     InstallApp(project.title)
            #     messages.success(request, 'Your site was successfully installed!')
            return redirect('project', project.owner, project.slug)
        
    context = {
        'dform': dform, 
        'sform': sform, 
        'project': project, 
        'profile': profile
    }
    return render(request, "projects/demo_form.html", context)


@login_required(login_url = "login")
# @unread_count()
def deleteProject(request, owner, slug):
    profile = request.user.profile
    project = profile.project_set.get(slug = slug)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
