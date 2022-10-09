from django.urls import path

from . import views

urlpatterns = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('new/', views.post_new, name='post_new'),
    path('delete/<int:post_id>', views.post_delete, name='post_delete'),
    path('edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('like/', views.post_like, name='post_like'),
]
