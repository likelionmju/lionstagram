from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects
    return render(request, 'home.html', {'posts':posts})

def post_detail(request, post_id):
    detail = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {'detail':detail})

def post_new(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST['title']
        post.author = request.user
        post.content = request.POST['content']
        # image 파일이 있으면 post 객체에 저장
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.pub_date = timezone.datetime.now()
        post.save()
        return redirect('/post/'+str(post.id))
    else:
        return render(request, 'post_new.html')
    