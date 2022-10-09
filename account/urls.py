from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('userpage/<str:author_id>', views.userpage, name='userpage'),
    path('changeprofile/', views.change_profile, name='change_profile'),
]
