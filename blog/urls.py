from django.urls import path

from . import views

from django.urls import include


app_name = 'blog'





urlpatterns = [

    path('',views.post_list,name='home'),

    path('<int:year>/<int:month>/<int:day>/<slug:postd>',views.post_detail,name='post_detail'),

    path('add_comment/<int:post_id>',views.post_comment,name='commentd'),

    path('category/<slug:category_slug>',views.post_list,name='category_detail'),

    path('dashboard/',views.dashboard,name='dashboard'),

    path('register/',views.user_registration,name='register')

    
]