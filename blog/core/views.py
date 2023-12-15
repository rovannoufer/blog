from django.shortcuts import render, redirect
from .models import Project
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

def blogs(request):
    blogs = Project.objects.all()
    context = {'blogs': blogs}
    return render(request, 'core/blogs.html', context)

def blog_project(request, pk):
    blog_project_obj = Project.objects.get(id=pk)
    tags = blog_project_obj.tags.all()
    return render(request, 'core/single-blog.html', {'blog': blog_project_obj, 'tags': tags})

@login_required(login_url='login')
def create_blog(request):
    profile = request.user.profile
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST)
    
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('blogs')
        
    context = {'form': form}
    return render(request, 'core/blogs_form.html',context)

@login_required(login_url='login')
def update_blog(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = BlogForm(instance=project)

    if request.method == 'POST':
        print(request.POST)
        form = BlogForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('blogs')
        
    context = {'form': form}
    return render(request, 'core/blogs_form.html',context)

@login_required(login_url='login')
def delete_blog(request, pk):
    profile = request.user.profile
    blogs = profile.project_set.get(id=pk)
    if request.method == 'POST':
        blogs.delete()
        return redirect('blogs')
    context ={'blogs':blogs}
    return render(request, 'core/delete_blog.html', context)