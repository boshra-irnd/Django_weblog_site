from django import forms
from django.contrib.postgres import search
from django.core import paginator
from django.db.models import query
from django.db.models.fields import AutoField
from django.db.models.query_utils import PathInfo
from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from .models import Post , Comment 
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm , CommentForm
from .forms import EmailPostForm , CommentForm, SearchForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector ,SearchQuery ,SearchRank
# Create your views here.


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 4
#     template_name = "blog/post/list.html"


def post_list(request,tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts , 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts":posts , 'page':page , "tag":tag}
    return render(request,'blog/post/list.html',context)



#/2021/3/20/second-blog
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status="published",publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    context = {'post':post,'form':comment_form ,'comments':comments, 's_posts':similar_posts}
    return render(request,'blog/post/detail.html',context)

def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status="published")
    if request.method =='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommended yor"
            message = f"{post.title} in {post_url} and {cd['comment']}"
            send_mail(
                subject,message,"weblog.ir@gmail.com",
                [cd['to']]
            )



    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form})


#search view
def post_search(request):
    form = SearchForm()
    query = None
    resault = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # A B C D => 1.0 , 0.4 , 0.2 , 0.1 
            search_vector = SearchVector('title', weight='A') + (SearchVector('body', weight='C'))
            search_query = SearchQuery(query)
            resault = Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.5).order_by('-rank')  
    return render(request, 'blog/post/search.html',{'form':form,'query':query,'resaults':resault}) 