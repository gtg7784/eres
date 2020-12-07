from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth

def index(request):
  status = {"isLogin": False}
  if request.user.is_authenticated:
    status = {"isLogin": True}

  return render(request, 'eres/index.html', status)

def category(request):
  category = request.GET.get('category', None)
  return render(request, 'eres/index.html', {category: category})

def generic(request):
  status = {"isLogin": False}
  if request.user.is_authenticated:
    status = {"isLogin": True}
  return render(request, 'eres/generic.html', status)

def post(request):
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
      print("LOGIN SUCCESS")
      return redirect("index")
    else:
      return render(request, 'eres/signin.html', {'error': '사용자의 ID 또는 비밀번호가 잘못되었습니다.'})
  return render(request, 'eres/signin.html')

@csrf_exempt
def signup(request):
  if request.method == "POST":
    username = request.POST.get("username", None)
    first_name = request.POST.get("first_name", None)
    password1 = request.POST.get("password1", None)
    password2 = request.POST.get("password2", None)

    if username is None:
      return render(request, "eres/signup.html", {"error": "아이디를 입력해주세요"})

    if first_name is None:
      return render(request, "eres/signup.html", {"error": "별명을 입력해주세요"})

    if password1 is None or password2 is None:
      return render(request, "eres/signup.html", {"error": "비밀번호를 입력해주세요"})

    if password1 == password2:
      user = User.objects.create_user(username=username, password=password1, first_name=first_name)
      user.save()
      auth.login(request, user)
      return redirect("index")

  return render(request, 'eres/signup.html')

def signout(request):
  auth.logout(request)
  return redirect("index")


def myinfo(request):
  info = {
    "username": request.user.username,
    "email": request.user.email,
    "first_name": request.user.first_name
  }

  if request.method == "POST":
    email = request.POST.get("email", None)
    first_name = request.POST.get("first_name", None)

    if first_name is None:
      return render(request, 'eres/myinfo.html', {"info": info, "error": "별명을 입력해주세요"})

    user = User.objects.all().filter(id=request.user.id)
    user.email = email
    user.first_name = first_name

    user.update()
    info["email"] = email
    info["first_name"] = first_name
    return render(request, 'eres/myinfo.html', {"info": info, "script": "정보가 수정되었습니다."})

  return render(request, 'eres/myinfo.html', {"info": info})

