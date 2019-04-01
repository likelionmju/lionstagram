from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects
    return render(request, 'home.html', {'posts':posts})