from django import template

from ..models import Post

from django.db.models import Count

register = template.Library()


@register.simple_tag()
def post_count():

    return Post.published.count()


@register.inclusion_tag('blog/post/includes/lat_post.html')
def lat_post(count=5):

    latest_post = Post.published.order_by('-publish')[:count]

    return {'lat_p':latest_post}

@register.inclusion_tag('blog/post/includes/get_most_com.html')
def get_mosted_comment(count=5):

    most_comm = Post.published.annotate(get_com=Count('comments')).\
    order_by('-get_com')[:count]

    return {'most_com':most_comm}



