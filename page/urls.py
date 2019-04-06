from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('new/', views.post_new, name='post_new'),
]