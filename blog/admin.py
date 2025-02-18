from django.contrib import admin

from blog.models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'author', 'publish')
    search_fields = ('title', 'slug', 'author', 'publish', 'status','published  date')
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug':('title',)}
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body',)