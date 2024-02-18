from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.postgres.search import TrigramSimilarity

from django.core.mail import send_mail

from django.views.decorators.http import require_POST

from django.views.generic import ListView

from taggit.models import Tag

from .models import Post,Comment,Gallery

from .forms import EmailShare,CommentForm,SearchForms

from django.db.models import Count



def post_list(request,tag_slug=None):

    post_l = Post.published.all()

    tag = None

    if tag_slug:
        
        tag = get_object_or_404(Tag,
                                slug=tag_slug)
        
        post_l = post_l.filter(tags__in=[tag])

    return render(request,'blog/post/index.html',{'posts':post_l,
                                                  'tag':tag})


def post_detail(request,year,month,day,postd):

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=postd,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    images = Gallery.objects.filter(post=post)
    
    form = CommentForm()

    comments = post.comments.filter(active=True)

    post_tags_ids = post.tags.values_list('id',flat=True)

    similar_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    similar_post = similar_post.annotate(same_tags=Count('tags'))\
    .order_by('-same_tags','-publish')[:4]



    return render(request,'blog/post/detail.html',{'details':post,
                                                   'form_comment':form,
                                                   'comments':comments,
                                                   'images':images,})



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