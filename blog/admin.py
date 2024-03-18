from django.contrib import admin

from .models import Category, Post,Comment,Gallery, Profile


class GalleryInline(admin.TabularInline):
    fk_name = 'post'
    model = Gallery

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug',  'publish', 'status']
    list_filter = ['status', 'created', 'publish',]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

    inlines = [GalleryInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name','slug']

    list_filter = ['created','updated','name']

    prepopulated_fields = {'slug':('name',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user','phone_number','date_of_birthy']

    raw_id_fields = ['user']

    search_fields = ['phone_number']