from django.urls import path

from blog import views
app_name = 'blog'  # Define the app name for URL namespace.


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
          views.post_detail, 
          name='post_detail'
    ),  # Add a URL for post detail page.
    path('<int:post_id>/share/', views.post_share, name='post_share'),  # Add a URL for post sharing.
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),  # Add a URL for commenting on a post.
    path('tag/<slug:tag_slug>/',views.post_list,name="post_list_by_tag")

]
