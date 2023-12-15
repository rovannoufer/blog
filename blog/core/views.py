from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import BlogForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def blogs(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    
    blogs = Project.objects.distinct().filter(
        Q(title__icontains = search_query) | Q(description__icontains = search_query) 
        | Q(owner__name__icontains = search_query) | Q(tags__in =tags))
    
    page = request.GET.get('page')
    results = 3
    
    paginator = Paginator(blogs, results)
    
    try:
       blogs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        blogs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        blogs = paginator.page(page)   

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        rightindex = paginator.num_pages + 1

    custom_range = range(left_index,right_index)
    context = {'blogs': blogs, 'paginator': paginator, 'custom_range': custom_range}
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