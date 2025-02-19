from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

from blog.models import Post,Comment
from blog.forms import EmailPostForm,CommentForm

def index(request):
    post = Post.objects.filter(title="Another post")
    print(post)
    print(post.query)
    return render(request, 'blog/base.html', {'posts': post})


def post_list(request,tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,  slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
      #  print(tag.name)
       
    paginator = Paginator(post_list, 3)  # Show 3 posts per page.
    page_number= request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    #print(tag.name)
    
    return render(
        request, 
        'blog/post_list.html', 
        {
            'posts': posts,
            'tag': tag,
        }
    )

def post_detail(request,year,month,day,post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,  # Filter posts published on specific day.
        status='published'  # Filter published posts only.
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    #list of similar posts
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    print(similar_posts)


    return render(
        request, 
        'blog/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts,
        }
    )


def post_share(request,post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status='published'
    )
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends your red {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments:{cd['email']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email='None',
                recipient_list=[cd['to']],
                fail_silently=False,  # Do not fail silently if sending fails.
            )
            sent = True
           
    else:
        form = EmailPostForm()
    return render(
        request, 
        'blog/post_share.html', 
        {
            'post': post, 
            'form': form,
            'sent':sent
        }
     )

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    comment = None
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.active = True  # Set active to True initially.
        comment.save()
        
   
    return render(
        request, 
        'blog/post_comment.html', 
        {
            'form': form,
            'post': post,
            'comment': comment
        }
    )