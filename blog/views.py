from django.core import paginator
from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts , 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{"posts":posts , 'page':page})

#/2021/3/20/second-blog
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status="published",publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/post/detail.html',{"post":post})