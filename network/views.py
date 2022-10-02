import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator
from .models import User, Post

def index(request):
    allPosts = Post.objects.all()
    paginator = Paginator(allPosts, 10)
    pageNumber = request.GET.get('page')
    onePagePosts = paginator.get_page(pageNumber)
    return render(request, "network/index.html",{
        "posts": onePagePosts,
        'pageNumRange': range(onePagePosts.paginator.num_pages)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def addPost(req):
    if req.method == "POST":
        content = req.POST.get("getPost")
        message = ''
        if content != '':
            Post.objects.create(content = content, owner = req.user)
            message = "Post Published"
        else:
            message = "Write Something"
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))


def getProfile(request, username):
    try:
        profile = User.objects.get(username = username)
    except:
        return render(request, 'network/404.html', {
            "message": "No user with this username"
        })       
    allPostsThisUser = profile.posts.all()
    paginator = Paginator(allPostsThisUser, 10)
    pageNumber = request.GET.get('page')
    onePagePosts = paginator.get_page(pageNumber)
    return render(request, 'network/profile.html', {
        "userprofile": profile,
        "following": profile.following,
        "followers": profile.followers,
        "allPosts": onePagePosts,
        'pageNumRange': range(onePagePosts.paginator.num_pages)
    })

def follow(request, userFollower, userFollowing):
    try:
        userToFollow = User.objects.get(username = userFollowing)
        flowerPerson = User.objects.get(username = userFollower)
    except:
        return render(request, 'network/404.html', {
            "message": "No user with this username"
        })
    flowerPerson.following.add(userToFollow)
    return HttpResponseRedirect(reverse("getProfile", kwargs={'username':userFollowing}))

def unFollow(request, userFollower, userFollowing):
    try:
        userToUnFollow = User.objects.get(username = userFollowing)
        flowerPerson = User.objects.get(username = userFollower)
    except:
        return render(request, 'network/404.html', {
            "message": "No user with this username"
        })
    flowerPerson.following.remove(userToUnFollow)
    return HttpResponseRedirect(reverse("getProfile", kwargs={'username':userFollowing}))

def getFollowingPost(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    person = User.objects.get(pk= request.user.id)
    followingPosts = Post.objects.filter(owner__in = person.following.all())
    
    paginator = Paginator(followingPosts, 10)
    pageNumber = request.GET.get('page')
    onePagePosts = paginator.get_page(pageNumber)
    return render(request, 'network/followingPosts.html',{
        "posts": onePagePosts,
        'pageNumRange': range(onePagePosts.paginator.num_pages)
    })
    
def updateLikes(request, postId):
    if request.user.is_authenticated:
        data = {}
        post = Post.objects.get(pk= postId)
        if request.user in post.lovers.all():
            data["type"] = "deleted"
            post.lovers.remove(request.user)
        else:
            data["type"] = "added"
            post.lovers.add(request.user)
        return JsonResponse(data, status = 200)
    else:
        return HttpResponseRedirect(reverse('login'))
@csrf_exempt
def editPost(request, postId):
    if request.user.is_authenticated:
        if Post.objects.filter(pk= postId).exists():
            post = Post.objects.get(pk = postId)
        if post.owner.id != request.user.id:
            return HttpResponseRedirect(reverse('index'))
        if request.method == "PUT":
            data = json.loads(request.body)
            if data.get("content") != '':
                post.content = data["content"]
                post.save()
                return JsonResponse({"message": "updated"})
            else:
                return JsonResponse({"message": "not found"})
    else:
        return HttpResponseRedirect(reverse('login'))