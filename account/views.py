from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from page.models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        if request.POST['pw'] == request.POST['confirm-pw']:
            user = User.objects.create_user(
                request.POST['id'], password=request.POST['pw']
            )
            auth.login(request, user)
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
    return render(request, 'userpage.html', {'posts':posts, 'user':user})
