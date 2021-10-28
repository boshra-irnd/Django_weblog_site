from django.core import paginator
from django.db.models import query
from django.shortcuts import render , get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = "blog/post/list.html"



#/2021/3/20/second-blog
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status="published",publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/post/detail.html',{"post":post})