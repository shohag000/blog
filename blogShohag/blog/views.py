from django.shortcuts import render, get_object_or_404,redirect
from .models import Article,Author,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import CreateForm,CreateUser,CreateAuthor,CreateCategory
from django.contrib import messages


from django.http import HttpResponse


def index(request):
    all_posts = Article.objects.all().order_by('-posted_on')
    search_kw= request.GET.get('search_kw')
    if search_kw:
        all_posts= all_posts.filter(
            Q(title__icontains=search_kw)|
            Q(body__icontains=search_kw)
        )
    paginator = Paginator(all_posts, 4)  # Show 4 posts per page

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    context = {
        "posts": posts
    }
    return render(request,"index.html",context)


def getAuthor(request,name):
    author_user=get_object_or_404(User,username=name)
    author = get_object_or_404(Author,name=author_user.id)
    posts = Article.objects.filter(article_author=author.id)
    
    context = {
        "posts": posts,
        "author": author
    }

    return render(request,"profile.html",context)

def getSingle(request,id):
    post = get_object_or_404(Article,pk=id)
    first= Article.objects.first()
    last=Article.objects.last()
    related_posts = Article.objects.filter(category=post.category).exclude(pk=post.id)[:4]
    context = {
        "post": post,
        "first":first,
        "last":last,
        "related_posts":related_posts
    }
    return render(request,"single.html",context)

def getTopic(request,name):
    category = get_object_or_404(Category,name=name)
    posts = Article.objects.filter(category=category.id)
    context = {
        "posts": posts,
        "category":category
    }
    return render(request,"category.html",context)


def getLogin(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            username = request.POST.get("user")
            password = request.POST.get("pass")

            auth = authenticate(request, username=username, password=password)
            if auth is not None:
                login(request, auth)
                messages.success(request, "Successfully login")
                return redirect("index")
            else:
                messages.error(request,"Username or Password not matched")
                return render(request, "login.html")

    return render(request,"login.html")

def getLogout(request):
    logout(request)
    messages.success(request, "Successfully logout")
    return redirect("index")

def getCreated(request):
    if request.user.is_authenticated:
        form = CreateForm(request.POST or None, request.FILES or None)
        article_author = get_object_or_404(Author,name=request.user.id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author= article_author
            instance.save();
            return redirect("index")
        context = {
            "form": form
        }
        return render(request, "create.html", context)
    else:
        return redirect("login")


def getProfile(request):
    if request.user.is_authenticated:
        user= get_object_or_404(User,id=request.user.id)
        author = Author.objects.get(name=user.id)
        if author:
            posts = Article.objects.filter(article_author=request.user.id)
            context = {
                "posts":posts,
                "author":author
            }
            return render(request,"logged_in_profile.html",context)
        else:
            form = CreateAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save();
                return redirect("profile")
            context={
                "form":form
            }
            return render(request,"create_author.html",context)
    else:
        return redirect("login")


def getUpdate(request,post_id):
    if request.user.is_authenticated:
        article_author = get_object_or_404(Author, name=request.user.id)
        post = get_object_or_404(Article, id=post_id)
        form = CreateForm(request.POST or None, request.FILES or None,instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author= article_author
            instance.save();
            messages.success(request,"Your post is successfully updated")
            return redirect("profile")
        context = {
            "form": form
        }
        return render(request, "create.html", context)
    else:
        return redirect("login")

def getDelete(request,deleted_post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Article,pk=deleted_post_id)
        post.delete()
        messages.success(request, "Your post is successfully deleted")
        return redirect("profile")
    else:
        return redirect("login")

def getRegister(request):
    form=CreateUser(request.POST or None)
    if form.is_valid():
        form.save(commit=False)
        form.save()
        return redirect("login")
    context = {
        "form":form
    }
    return render(request,"register.html",context)


def getCreatedCategory(request):
    if request.user.is_authenticated:
        form= CreateCategory(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect("create")
        context= {
            "form": form
        }
        return render(request,"create_category.html",context)
    return redirect("index")

def getCategoryList(request):
    categories = Category.objects.all()
    context = {
        "categories":categories
    }
    return render(request,"category_list.html",context)

