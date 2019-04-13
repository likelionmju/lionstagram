from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post

# import Json
try:
    from django.utils import simplejson as json
except ImportError:
    import json

def home(request):
    posts = Post.objects
    return render(request, 'home.html', {'posts':posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'post':post})

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
            return render(request, 'post_edit.html', {'post':post})
        else:
            return redirect('home')
        
# 좋아요 구현
def like(request, post_id):
    post=get_object_or_404(Post, pk=post_id) # 해당 포스트
    user=request.user

    if post.likes.filter(id=user.id).exists(): 
        post.likes.remove(user)
    else:
        post.likes.add(user)
        
    return redirect('home')
