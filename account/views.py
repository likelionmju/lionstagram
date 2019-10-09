from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from page.models import Post
from account.models import Profile

from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
def register(request):
    if request.method == 'POST':
        if request.POST['pw'] == request.POST['confirm-pw']:
            user = User.objects.create_user(
                request.POST['id'], password=request.POST['pw']
            )
            auth.login(request, user)
            profile = Profile()
            profile.user = request.user
            profile.image = os.path.join(BASE_DIR, '/default/lion_profile.jpg')
            profile.save()
            return redirect('home')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['pw']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect ('home')
        else:
            return HttpResponse('입력 정보를 확인하세요.')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def userpage(request, author_id):
    # 유저 객체를 user에 저장
    user = User.objects.get(username=author_id)
    # 해당 유저의 포스트만 불러오기
    posts = Post.objects.filter(author=user)
    profile = Profile.objects.filter(user=user)
    return render(request, 'userpage.html', {'posts':posts, 'user':user, 'profile':profile})


def change_profile(request):
    # if profile_image exist, delete this image 
    if Profile.objects.filter(user=request.user):
        Profile.objects.filter(user=request.user).delete()

    profile = Profile()
    profile.user = request.user
    # save profile_image
    if 'image' in request.FILES:
        im = Image.open(request.FILES['image'])
        im = im.resize((1920, 1920));
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        
        buffer = BytesIO()
        output.save(buffer, format='png')

        file = InMemoryUploadedFile(
            buffer,
            '{}'.format(request.FILES['image']),
            '{}'.format(request.FILES['image']),
            'image/png',
            buffer.tell(),
            None,
        )

        profile.image = file
    profile.save()
    return redirect('/account/userpage/'+str(profile.user))