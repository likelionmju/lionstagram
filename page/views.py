import json
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST
from PIL import Image

from .models import Like
from .models import Post
from account.models import Profile


def home(request):
    posts = Post.objects
    profiles = Profile.objects
    return render(request, 'home.html', {'posts': posts, 'profiles': profiles})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    profile = Profile.objects.filter(user=post.author)
    return render(
        request, 'post_detail.html', {'post': post, 'profile': profile},
    )


def post_new(request):
    # 작성 폼 제출
    if request.method == 'POST':
        post = Post()
        post.author = request.user
        post.content = request.POST['content']
        # image 파일이 있으면 post 객체에 저장
        if 'image' in request.FILES:
            image = Image.open(request.FILES['image'])
            exif = image._getexif()
            orientation_key = 274  # cf ExifTags

            if exif and orientation_key in exif:
                orientation = exif[orientation_key]

                rotate_values = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90,
                }

                if orientation in rotate_values:
                    image = image.transpose(rotate_values[orientation])

                buffer = BytesIO()
                image.save(buffer, format='png')

                file = InMemoryUploadedFile(
                    buffer,
                    '{}'.format(request.FILES['image']),
                    '{}'.format(request.FILES['image']),
                    'image/png',
                    buffer.tell(),
                    None,
                )
            post.image = file
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
    post_like, post_like_created = Like.objects.get_or_create(
        user=request.user, post=post,
    )

    if not post_like_created:
        post_like.delete()

    # Like count
    likes_count = Like.objects.filter(post=post, post_id=pk).count()
    content = {'likes_count': likes_count}
    return HttpResponse(json.dumps(content))
