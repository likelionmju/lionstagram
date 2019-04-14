from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Like
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def home(request):
    posts = Post.objects
    mylikes = Like.objects.filter(user=request.user)
    return render(request, 'home.html', {'posts': posts, 'mylikes':mylikes})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})


def post_new(request):
    # 작성 폼 제출
    if request.method == 'POST':
        post = Post()
        post.author = request.user
        post.content = request.POST['content']
        # image 파일이 있으면 post 객체에 저장
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.pub_date = timezone.datetime.now()
        post.save()
        return redirect('/post/'+str(post.id))
    # 작성 폼
    else:
        return render(request, 'post_new.html')


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
        return redirect('home')
    else:
        return redirect('post_detail', post_id)


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # 수정 폼 제출
    if request.method == 'POST':
        post.content = request.POST['content']
        # image 파일이 있으면 post 객체에 저장
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        return redirect('/post/'+str(post.id))
    else:
        # 수정 폼
        if post.author == request.user:
            return render(request, 'post_edit.html', {'post': post})
        else:
            return redirect('home')

# 좋아요 구현
@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)  # 좋아요 버튼 id 가져오기
    post = get_object_or_404(Post, pk=pk)  # 해당 포스트

    # Like create
    post_like, post_like_created = Like.objects.get_or_create(user=request.user, post=post)

    if not post_like_created:
        post_like.delete()

    # Like count
    likes_count = Like.objects.filter(post=post, post_id=pk).count()
    content = {'likes_count': likes_count} 
    return HttpResponse(json.dumps(content))
