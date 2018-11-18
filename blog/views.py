from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .models import Comment
from .forms import PostForm
from .forms import CommentForm
from django.shortcuts import redirect


def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    comments = Comment.objects.filter(post=post).order_by("published_date")
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def comment_new(request, postId):
    post_comment = get_object_or_404(Post, pk=postId)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.author = request.user
            comment.post = post_comment
            comment.published_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk = postId)
    else:
        form = CommentForm()
    return render(request, 'blog/comment.html', {'form':form})
