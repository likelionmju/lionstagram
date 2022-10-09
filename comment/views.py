from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone

from .models import Comment
from page.models import Post

# Create your views here.


def comment_new(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        comment = Comment()
        comment.content = request.POST['comment']
        comment.title = post
        comment.author = request.user
        comment.pub_date = timezone.now()
        comment.save()
    return redirect('post_detail', post_id)


def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', post_id)
