from django.urls import path
from . import views

urlpatterns = [
    path('new/<int:post_id>', views.comment_new, name='comment_new'),
    path('delete/<int:post_id>/<int:comment_id>', views.comment_delete, name='comment_delete'),
]