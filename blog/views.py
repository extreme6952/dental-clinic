from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.postgres.search import TrigramSimilarity

from django.core.mail import send_mail

from django.views.decorators.http import require_POST

from django.views.generic import ListView

from taggit.models import Tag

from .models import Category, Post,Comment,Gallery

from .forms import EmailShare,CommentForm,SearchForms

from django.db.models import Count



def post_list(request,category_slug=None):

    post_l = Post.published.all()

    category = None

    categories = Category.objects.all()


    if category_slug:

        category = get_object_or_404(Category,
                                     slug=category_slug)
        
        post_l = post_l.filter(category=category)
    



    return render(request,'blog/post/index.html',{'posts':post_l,
                                                  'category':category,
                                                  'categories':categories})


def post_detail(request,year,month,day,postd,
                category_slug=None):

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


    return render(request,'blog/post/detail.html',{'details':post,
                                                   'form_comment':form,
                                                   'comments':comments,
                                                   'images':images,
                                                   'categories':categories,
                                                   'category':category})

# def category_list(request,category_slug=None):

#     category = None

#     categories = Category.objects.all()

#     if category_slug:

#         categories = get_object_or_404(Category,
#                                      slug=category_slug)
        
#         post = Post.published.filter(category=category)

#     return render(request,
#                   'blog/post/includes/navbar.html',
#                   {'post_cat':post,
#                    'categories':categories,
#                    'category':category})



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


def post_search(request):

    query = None

    results = [ ]

    if 'query' in request.GET:

        form = SearchForms(request.GET)

        if form.is_valid():

            query = form.cleaned_data

            results = Post.published.annotate(search=TrigramSimilarity('title',query)
                                              ).filter(search__gt=0.1).order_by('-search')
            
    
    return render(request,
                  'blog/post/search.html',
                  {'form_search':form,
                   'results':results,
                   'query':query})