import os, sys
from pathlib import Path
from django.conf import settings


def getAvailableProjects():
    available_demos = []
    demo_projects = os.scandir(settings.DEMOS_ROOT)
    for project in demo_projects:
        if project.is_dir():
            available_demos.append(project)
    return available_demos


def getProjectDir(project, name = 'manage.py'):
    project_dir = None
    proj_first_lvl_path = os.path.join(settings.DEMOS_ROOT, project)
    project_first_level = os.scandir(proj_first_lvl_path)
    for entry in project_first_level:
        if entry.is_file() and entry == name:
            project_dir = proj_first_lvl_path
            return project_dir
        # TODO:Complete recursive function to parse directory


# def assignProjectDir(obj, path):
#     obj.domain = f"http://{settings.PARENT_HOST}/{obj.slug}"
#     pass


def cloneProject(uri, slug):
    path = uri.split('/')
    project_name = path[-1]
    project_path = os.path.join(settings.DEMOS_ROOT, slug)
    if not slug in os.scandir(settings.DEMOS_ROOT):
        if os.getcwd() != settings.DEMOS_ROOT:
            os.chdir(settings.DEMOS_ROOT)
        try:
            os.mkdir(project_path)
        except:
            print('Could not create directory {slug}')
            return
    
    if not project_name in os.scandir(project_path):
        if os.getcwd() != project_path:
            os.chdir(project_path)
        try:
            os.system('git clone {uri}\n')
        except:
            print('Could not cloane {uri}\n')



# def DirFinder(path, name):
#     for item in os.listdir(path):
#         if os.path.isfile(os.path.join(path, item)) and name == item:
#             return path
#         elif os.path.isdir(os.path.join(path, item)) and name == item:
#             return path
#         else:
#             DirFinder(os.path.join(path, item), name)

# for item in os.listdir(PROJECTS_DIR):
#     site_dir = ''  # site_dir: path for site directory (directory containing settings.py)
#     project_dir = ''  # project_dir: path for project directory (directory containing manage.py)
#     project_dir = ''  # project_dir: path for project directory (directory containing manage.py)
#     app_dirs = []  # app_dirs: names of the application directories in the project
#     project_name = '' 
    
#     if os.path.isdir(os.path.join(PROJECTS_DIR, item)):
#         path = os.path.join(PROJECTS_DIR, item)
#         project_dir = DirFinder(path, 'manage.py')
#         site_dir = DirFinder(path, 'settings.py')
#         app_dirs = AppFinder(project_dir, project_dir.split('/')[-1], site_dir.split('/')[-1])
        
#         project_name = 'static.projects.%s' % item

#     if project_name not in INSTALLED_APPS:
#         INSTALLED_APPS = INSTALLED_APPS+(project_name,)

#     template_dir = os.path.join(PROJECTS_DIR, '%s/templates/' % item)

#     if os.path.isdir(template_dir):
#         if template_dir not in TEMPLATE_DIRS:
#             TEMPLATE_DIRS = TEMPLATE_DIRS+(template_dir,)

#     static_files_dir = os.path.join(PROJECTS_DIR, '%s/static/' % item)

#     if os.path.isdir(static_files_dir):
#         if static_files_dir not in STATICFILES_DIRS:
#             STATICFILES_DIRS = STATICFILES_DIRS + (static_files_dir,)