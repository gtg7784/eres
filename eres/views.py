from .models import Post
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from .forms import PostForm

def index(request):
  isLogin = False
  if request.user.is_authenticated:
    isLogin = True

  try:
    posts = Post.objects.all()
    return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts})
  except:
    pass

  return render(request, 'eres/index.html', {"isLogin": isLogin})

def category(request, category):
  isLogin = False
  if request.user.is_authenticated:
    isLogin = True

  print(f"category: {category}")

  posts = Post.objects.filter(category=category)
  
  if not posts.exists():
    return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts, "script": "해당 카테고리의 게시글이 없습니다."})

  return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts})

def generic(request, post_id):
  isLogin = False
  if request.user.is_authenticated:
    isLogin = True

  try:
    post = Post.objects.get(id=post_id)
  except:
    return render(request, 'eres/404.html')

  return render(request, 'eres/generic.html', {"isLogin": isLogin, "post": post})

@csrf_exempt
def post(request):
  if not request.user.is_authenticated:
    return redirect("eres:index")

  if request.method == "POST":
    title = request.POST.get("title", "")
    contents = request.POST.get("contents", "")
    category = request.POST.get("category", "")
    author = request.user.first_name

    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.title = title
      post.contents = contents
      post.category = category
      post.author = author
      post.save()

      return redirect("eres:index")
    else:
      post = Post(title=title, contents=contents, category=category, author=author)
      post.save()
      return redirect("eres:index")
  return render(request, 'eres/post.html')

@csrf_exempt
def signin(request):
  if request.method == "POST":
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)

    if username is None:
      return render(request, 'eres/signin.html', {'error': 'ID를 입력해주세요'})
    if password is None:
      return render(request, 'eres/signin.html', {'error': '비밀번호를 입력해주세요'})

    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect("eres:index")
    else:
      return render(request, 'eres/signin.html', {'error': '사용자의 ID 또는 비밀번호가 잘못되었습니다.'})
  return render(request, 'eres/signin.html')

@csrf_exempt
def signup(request):
  if request.method == "POST":
    username = request.POST.get("username", "")
    first_name = request.POST.get("first_name", "")
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")

    if username == "":
      return render(request, "eres/signup.html", {"error": "아이디를 입력해주세요"})

    if first_name == "":
      return render(request, "eres/signup.html", {"error": "별명을 입력해주세요"})

    if password1 == "" or password2 == "":
      return render(request, "eres/signup.html", {"error": "비밀번호를 입력해주세요"})

    if password1 == password2:
      try:
        user = User.objects.create_user(username=username, password=password1, first_name=first_name)
        user.save()
        auth.login(request, user)
        return redirect("eres:index")
      except Exception:
        return render(request, 'eres/signup.html', {"error": "아이디가 중복되었습니다 "})
    else:
      return render(request, 'eres/signup.html', {"error": "비밀번호가 다릅니다. "})

  return render(request, 'eres/signup.html')

def signout(request):
  auth.logout(request)
  return redirect("eres:index")


def myinfo(request):
  if not request.user.is_authenticated:
    return redirect("eres:index")

  info = {
    "username": request.user.username,
    "email": request.user.email,
    "first_name": request.user.first_name
  }

  posts = Post.objects.all().filter(author=request.user.username)

  if request.method == "POST":
    email = request.POST.get("email", None)
    first_name = request.POST.get("first_name", None)

    if first_name is None:
      return render(request, 'eres/myinfo.html', {"info": info, "error": "별명을 입력해주세요", "isLogin": True})

    user = User.objects.all().filter(id=request.user.id)
    user.email = email
    user.first_name = first_name

    user.update()
    info["email"] = email
    info["first_name"] = first_name

    return render(request, 'eres/myinfo.html', {"info": info, "script": "정보가 수정되었습니다.", "isLogin": True})

  return render(request, 'eres/myinfo.html', {"info": info, "posts": posts, "isLogin": True})

