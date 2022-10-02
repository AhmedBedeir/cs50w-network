
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPost",views.addPost, name="addPost"),
    path('profile/<str:username>', views.getProfile, name="getProfile"),
    path('follow/<str:userFollower>/<str:userFollowing>', views.follow, name="follow"),
    path('unfollow/<str:userFollower>/<str:userFollowing>', views.unFollow, name="unFollow"),
    path('following/posts', views.getFollowingPost, name="followingPosts"),
    path('love/<int:postId>', views.updateLikes, name="love"),
    path('edit/<int:postId>', views.editPost, name="edit"),
]
