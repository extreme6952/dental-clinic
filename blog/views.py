from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.postgres.search import TrigramSimilarity,SearchVector,SearchQuery,SearchRank

from django.core.mail import send_mail

from django.views.decorators.http import require_POST

from django.views.generic import ListView

from taggit.models import Tag

from .models import Category, Post,Comment,Gallery, Profile

from .forms import EmailShare,CommentForm,SearchForms,\
                    UserEditForm,ProfileEditForm,UserRegistrationForm

from django.db.models import Count

from django.contrib.auth.decorators import login_required

from django.contrib import messages


@login_required
def post_list(request,category_slug=None):

    post_l = Post.published.all()

    category = None

    categories = Category.objects.all()


    if category_slug:
   
        category = get_object_or_404(Category,
                                     slug=category_slug)
        
        post_l = post_l.filter(category=category)
    
                
    form_search = SearchForms() 

    return render(request,'blog/post/index.html',{'posts':post_l,
                                                  'category':category,
                                                  'categories':categories,
                                                  'form_search':form_search})




@login_required
def category_list(request,category_slug=None):

    categories = Category.objects.all()

    category = None

    if category_slug:

        category = get_object_or_404(Category,
                                     slug=category_slug)
        
        post_l = Post.published.filter(category=category)

    return render(request,
                  'blog/post/category_list.html',
                  {'category':category,
                   'post_l':post_l,
                   'categories':categories})










@login_required
def post_detail(request,year,month,day,postd,category_slug=None):

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=postd,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    category = None

    categories = Category.objects.all()

    if category_slug:

        category = get_object_or_404(Category,
                                     slug=category_slug)
        
        post = post.filter(category=category)
    
    images = Gallery.objects.filter(post=post)
    
    form = CommentForm()

    comments = post.comments.filter(active=True)

    form_search = SearchForms()


    return render(request,'blog/post/detail.html',{'details':post,
                                                   'form_comment':form,
                                                   'comments':comments,
                                                   'images':images,
                                                   'categories':categories,
                                                   'category':category,
                                                   'form_search':form_search})

def category_list(request,category_slug=None):

    post = Post.published.all()

    category = None

    categories = Category.objects.all()

    if category_slug:

        categories = get_object_or_404(Category,
                                     slug=category_slug)
        
        post = post.filter(category=category)

    return render(request,
                  'blog/post/includes/navbar.html',
                  {'post_cat':post,
                   'categories':categories,
                   'category':category})



@require_POST
def post_comment(request,post_id):

    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    
    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():

        comment = form.save(commit=False)

        comment.post = post

        comment.save()

    return render(request,'blog/post/comment.html',{'post':post,
                                                    'comment':comment,
                                                    'form_comment':form})



@login_required
def dashboard(request,category_slug=None):

    post_l = Post.published.all()

    category = None

    categories = Category.objects.all()


    if category_slug:
   
        category = get_object_or_404(Category,
                                     slug=category_slug)
        
        post_l = post_l.filter(category=category)

    return render(request,
                  'account/dashboard.html',
                  {'dashboard':'section',
                   'category':category,
                   'categories':categories,
                    'post_l':post_l})

def user_registration(request):

    if request.method=='POST':
        
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():

            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password'])
    
            new_user.save()

            Profile.objects.create(user=new_user)

            return redirect('blog:dashboard')

    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/user_registration_form.html',
                  {'user_form':user_form})




@login_required
def user_edit_account(request):

    if request.method=='POST':

        user_form = UserEditForm(data=request.POST,
                                 instance=request.user)

        profile_form = ProfileEditForm(data=request.POST,
                                       instance=request.user.profile_users,
                                       files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            
            profile_form.save()

            messages.success(request,'Вы успешно изменили свои данные')

            return redirect('blog:dashboard')
        
        else:

            messages.error(request,'Что-то пошло не так :(')

    else:

        user_form = UserEditForm(instance=request.user)

        profile_form = ProfileEditForm(instance=request.user.profile_users)

    return render(request,
                  'account/user_edit_form.html',
                  {'profile_form':profile_form,
                   'user_form':user_form})






def post_search(request):

    form_search = SearchForms()

    query = None

    results = [ ]

    if 'query' in request.GET:

        form_search = SearchForms(request.GET)

        if form_search.is_valid():

            query = form_search.cleaned_data['query']

            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
                ).filter(search=query)
        
    return render(request,
                  'blog/post/search.html',
                  {'form_search':form_search,
                   'query':query,
                   'results':results})