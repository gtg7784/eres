from .models import Post
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import PostForm

# 이것은 index 함수입니다.
def index(request):
  isLogin = False
  # request.user.is_authenticated 에 값이 있으면, 사용자가 로그인을 한것입니다.
  if request.user.is_authenticated:
    # isLogin 변수를 True로 바꿔줍니다.
    # 이게 왜 필요하냐구요? templates 안에 있는 eres/menu.html 에 보면,
    # 로그인을 했으면 내정보랑, 로그아웃이 들어가고, 로그인을 안했으면 로그아웃 대신에 로그인이 뜨기 때문입니다
    isLogin = True

  # templates에서 검색을 form 테그의 get 함수로 처리했습니다.
  query = request.GET.get('query', '')

  # get 요청을 받고, 요청에 query 인자가 있으면, 아래 if 문이 실행됩니다.
  if query:
    # query는 검색어가 들어가는 부분입니다.

    # filter 를 통해서, 검색어가 들어간 부분을 가져옵니다.
    # 모델 안에 있는 값 __icontains 를 하면 포함되어 있는 값을 가져옵니다.
    posts = Post.objects.filter(title__icontains=query) 
    
    # query 안에 있는 값이 title 에 포함되어 있는 모델만 가지고 와서 context에 넣어주고 render 합니다.
    return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts})    

  try:
    # 이거는 query가 없을 때 post를 가져오는 부분입니다.
    # Post.objects.all() 을 통해, post 모델에 있는 모든 값을 가져옵니다.
    posts = Post.objects.all()
    return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts})
  except:
    # post 에 값이 없으면, python에서 에러를 뿜기 때문에, try-except 문으로 처리를 했습니다.
    pass

  # post 값이 없기 때문에, context에 post 없이 render 해줍니다.
  return render(request, 'eres/index.html', {"isLogin": isLogin})

# category 함수입니다.
def category(request, category):
  isLogin = False
  
  # request.user.is_authenticated 에 값이 있으면, 사용자가 로그인을 한것입니다.
  if request.user.is_authenticated:
    # isLogin 변수를 True로 바꿔줍니다.
    # 이게 왜 필요하냐구요? templates 안에 있는 eres/menu.html 에 보면,
    # 로그인을 했으면 내정보랑, 로그아웃이 들어가고, 로그인을 안했으면 로그아웃 대신에 로그인이 뜨기 때문입니다
    isLogin = True

  # category 함수의 두번째 인자값인, category 인자를 기준으로, filter를 합니다.
  posts = Post.objects.filter(category=category)
  
  # post가 존재하지 않으면,
  if not posts.exists():

    # context에 경고창에 띄울 내용을 넣어서 render 합니다.
    # 그러면 템플릿에서 script 테그를 실행합니다.
    return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts, "script": "해당 카테고리의 게시글이 없습니다."})

  # post가 존재하면, 정상적으로 값을 보내줍니다.
  return render(request, 'eres/index.html', {"isLogin": isLogin, "posts": posts})

# generic 함수입니다.
def generic(request, post_id):
  isLogin = False

  # request.user.is_authenticated 에 값이 있으면, 사용자가 로그인을 한것입니다.
  if request.user.is_authenticated:
    # isLogin 변수를 True로 바꿔줍니다.
    # 이게 왜 필요하냐구요? templates 안에 있는 eres/menu.html 에 보면,
    # 로그인을 했으면 내정보랑, 로그아웃이 들어가고, 로그인을 안했으면 로그아웃 대신에 로그인이 뜨기 때문입니다
    isLogin = True

  try:
    # generic 함수의 두번째 인자값인 post_id 를 받아서, Post 모델에서 하나만 값을 가져옵니다 (Model.objects.get 함수 사용)
    post = Post.objects.get(id=post_id)
  except:
    # try-except 문을 사용해서, post에 값이 존재하지 않으면, 404 페이지를 render 합니다.
    return render(request, 'eres/404.html')

  # request의 method가 POST일 때입니다.
  if request.method == "POST":
    # 템플릿에서 삭제 버튼을 form으로 처리했기 때문에 post.delete 해줍니다.
    post.delete()
    # 그러고 context에 script를 넣어서, 똑같이 처리를 해줍니다.
    return render(request, 'eres/generic.html', {"isLogin": isLogin, "post": post, "script": "게시글이 삭제되었습니다."})

  # 만약, 로그인을 했으면
  if isLogin:
    # context에 me 인자를 넣어줍니다. 이를 통해서 사용자가 게시글을 작성한 사람인지 아닌지를 템플릿에서
    # 확인 한 후에, 게시글을 작성한 사람이면, 삭제 버튼을 보여줍니다.
    return render(request, 'eres/generic.html', {"isLogin": isLogin, "post": post, "me": request.user.first_name})

  # 이거는 전부 아닐때, 삭제버튼 없이 정상적으로 보여주게 됩니다.
  return render(request, 'eres/generic.html', {"isLogin": isLogin, "post": post})

# post 함수입니다.
@csrf_exempt
def post(request):
  if not request.user.is_authenticated:
    # 포스팅은, 사용자가 로그인을 했을때만 작성 할 수 있기 때문에
    # redirect로 위에 있는 index 함수로 넘깁니다.
    return redirect("eres:index")
  
  # request의 method가 POST 일 때
  if request.method == "POST":
    # POST 요청안에 들어있는 값들(title, contents, category, user.first_name(별명)) 을 가져온담에
    title = request.POST.get("title", "")
    contents = request.POST.get("contents", "")
    category = request.POST.get("category", "")
    author = request.user.first_name

    # 파일 업로드는 Model Form 을 사용해서 처리했습니다.
    # forms.py 에 작성한 PostForm 이라는 이름의 ModelForm을 가져와서 처리를 해줍니다.
    form = PostForm(request.POST, request.FILES)

    # ModelForm 안에 is_valid를 통해 파일이 들어가있는지 확인하고
    if form.is_valid():
      # 있으면, PostForm을 save 해준다, 이때, 인자에 commit을 False로 해서, 모델에 저장이 안되게 한다.
      post = form.save(commit=False)
      # 왜냐하면, ModelForm을 통해 title과 file만 들어가있기 때문에
      # 아래 내용들을 채워주고
      post.title = title
      post.contents = contents
      post.category = category
      post.author = author
      # 여기서 save를 한다.
      post.save()

      # 포스팅이 다 되고 모델에 저장이 되면 index로 redirect한다.
      return redirect("eres:index")
    else:
      # 파일이 없을 때, file 없이 Post 모델을 생성한다.
      post = Post(title=title, contents=contents, category=category, author=author)
      # post 모델을 저장한다.
      post.save()

      # 포스팅이 다 되고 모델에 저장이 되면 index로 redirect한다.
      return redirect("eres:index")

  # request의 method가 GET 일 때, post.html 을 렌더한다.
  # 이때 context의 isLogin이 왜 True냐고 물으면, 로그인을 
  # 하지 않았을때는 위에서 알아서 index로 처리해주기 때문이다.
  # views.py 106번째 줄 참조.
  return render(request, 'eres/post.html', {"isLogin": True})

# signin 함수입니다.
@csrf_exempt
def signin(request):
  # request의 method가 POST 일 때
  if request.method == "POST":
    # 이름이랑 비밀번호 받아와서
    username = request.POST.get("username", '')
    password = request.POST.get("password", '')

    # 이름이랑 비밀번호 있는지 검사하고, 없으면 context에 error 넣어서 render
    if username == '':
      return render(request, 'eres/signin.html', {'error': 'ID를 입력해주세요'})
    if password == '':
      return render(request, 'eres/signin.html', {'error': '비밀번호를 입력해주세요'})

    # 이름이랑 비밀번호 둘 다 있으면, django에서 기본적으로 제공해주는
    # auth 모듈의 authenticate(한국어로 하면 인증이라는 뜻) 함수를 통해서 인증을 해준다
    user = auth.authenticate(request, username=username, password=password)

    # user가 None이 아니면(== user가 존재하면)
    if user is not None:
      # 로그인 해주고
      auth.login(request, user)
      # redirect
      return redirect("eres:index")
    else:
      # user가 None이면(== user가 존재하지 않으면)
      # context에 error 담아서 render
      return render(request, 'eres/signin.html', {'error': '사용자의 ID 또는 비밀번호가 잘못되었습니다.'})
      
  # get method 일 땐, signin render
  return render(request, 'eres/signin.html')

@csrf_exempt
def signup(request):
  # request의 method가 POST 일 때
  if request.method == "POST":
    # 이름, 별명, 비밀번호 1, 2 받아와서
    username = request.POST.get("username", "")
    first_name = request.POST.get("first_name", "")
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")

    # 없으면 없다해주고
    if username == "":
      return render(request, "eres/signup.html", {"error": "아이디를 입력해주세요"})
    if first_name == "":
      return render(request, "eres/signup.html", {"error": "별명을 입력해주세요"})
    if password1 == "" or password2 == "":
      return render(request, "eres/signup.html", {"error": "비밀번호를 입력해주세요"})

    # 비밀번호랑 비밀번호 확인 같으면
    if password1 == password2:
      try:
        # user 생성
        # User은 모델을 만들어 준게 아니라. django 에서 제공해주는 모델을 썼다.
        # 별명을 따로 custom으로 만들기 싫어서, first_name 에다가 별명을 넣어준다.
        user = User.objects.create_user(username=username, password=password1, first_name=first_name)
        # 저장!
        user.save()
        # 로그인!
        auth.login(request, user)
        # index로 redirect
        return redirect("eres:index")
      except:
        # 이 과정에서 에러가 발생하면, 아이디가 중복되었디는 소리기 때문에 error 넣어서 render
        # try-except 문을 사용해서 관리함
        return render(request, 'eres/signup.html', {"error": "아이디가 중복되었습니다 "})
    else:
      # 비밀번호 다른지 확인
      return render(request, 'eres/signup.html', {"error": "비밀번호가 다릅니다. "})

  # request method == get
  return render(request, 'eres/signup.html')

# signout 함수
def signout(request):
  # 로그아웃해
  auth.logout(request)
  # index로 redirect
  return redirect("eres:index")

# myinfo 함수
def myinfo(request):
  if not request.user.is_authenticated:
    # 내정보는, 사용자가 로그인을 했을때만 작성 할 수 있기 때문에,
    # redirect로 위에 있는 index 함수로 넘깁니다.
    return redirect("eres:index")

  # info에 딕셔너리 형태로 아이디, 이메일, 별명 받아줌
  info = {
    "username": request.user.username,
    "email": request.user.email,
    "first_name": request.user.first_name
  }

  # Post 모델에 내가 쓴 거 filter로 내가 작성한 것들 가져옴
  posts = Post.objects.all().filter(author=request.user.username)

  # request의 method가 POST 일 때
  if request.method == "POST":
    # 이메일이랑 별명 받아서
    email = request.POST.get("email", '')
    first_name = request.POST.get("first_name", '')

    if first_name == '':
      # 별명은 무조건 입력해야 하기 때문에, error를 context에 넣어주고 render
      return render(request, 'eres/myinfo.html', {"info": info, "isLogin": True, "error": "별명을 입력해주세요"})

    # id 를 기준으로 맞는거 찾고
    user = User.objects.all().get(id=request.user.id)
    user.email = email
    user.first_name = first_name

    # update
    user.update()
    # info 딕셔너리에 업데이트 해서
    info["email"] = email
    info["first_name"] = first_name

    # render할 때 context에 script 넣어서 보냄
    return render(request, 'eres/myinfo.html', {"info": info, "isLogin": True, "script": "정보가 수정되었습니다."})

  # get 일때
  return render(request, 'eres/myinfo.html', {"info": info, "posts": posts, "isLogin": True})

