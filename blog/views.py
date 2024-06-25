"""from django.shortcuts import render

# Create your views here.
def index(request):
     return render(request,'index.html')"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
from blog.models import Post, Comment
from django.http import HttpResponseRedirect
from blog.forms import CommentForm
  
  
#################### index####################################### 
def index(request):
    return render(request, 'index.html', {'title':'index'})
  
########### register here ##################################### 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            htmly = get_template('Email.html')
            d = { 'username': username }
            subject, from_email, to = 'Email Confirmation', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title':'register here'})
  
# login forms#
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('slideshow')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form':form, 'title':'log in'})


def slideshow(request):
    # view logic here
    return render(request, 'slideshow.html')
    
def home(request):
    return render(request, 'home.html')
def post(request):
    return render(request, 'post.html')
def contact(request):
    return render(request, 'contact.html')
def aindex(request):
    return render(request, 'aindex.html')

def post_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "postindex.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)
   
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
         "comments": comments,
        "form": CommentForm(),
    }
    

    return render(request, "detail.html", context)
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Post

@require_POST
def update_like(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'status': 'success', 'likes': post.likes})
    return JsonResponse({'status': 'error', 'message': 'Post ID not provided or invalid'})