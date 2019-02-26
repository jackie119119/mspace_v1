from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm  # added in 12.26
from django.http import HttpResponse

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # list comments here 12.26 by Jackie
    comments = post.comments.filter(active=True)  #got all active comments related to specifed post to variable 'comments'.
    new_comment = None  #initiate a virable.
    if request.method == 'POST':
        # a comment was posted. instantiate comment form.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        # if this is not posted senario, initialize the form.
        comment_form = CommentForm()
    # end 12.26 comment here

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments':comments,   #added in 12.26
                   'new_comment':new_comment,   #added in 12.26 
                   'comment_form':comment_form  #added in 12.26
                   })


#this is a method to use class rather than def function as the view modules.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# this following code is for test use. 2018.12.25 by Jackie
# comparing with book example, this code remove post part.
def post_share(request):
    if request.method == 'POST':
        # when form is filled and submitted by post method.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd = cd['name']
            return HttpResponse(cd)
            # code for sending email
    else:  # this is for initialize the form by create a instance.
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form})

