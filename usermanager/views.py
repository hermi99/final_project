from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from usermanager.forms import LoginForm, RegisterForm
from usermanager.models import Users
from django.contrib.auth import login, logout, authenticate

@login_required(login_url='/login')
def index(request):
    user = Users.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymous User!"
    print("Logged in?", request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "Anonymous User!"
    print(email)
    return render(request, "index.html", {"user": user, "welcome_msg": "Hello FastCampus!"})

def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me

                    # if not remember_me:
                    #     request.session.set_expiry(0)

                    return redirect('/')
    else:
        msg = None
        form = LoginForm()
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    logout(request)
    return redirect("/")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        # return render(request, "register.html", {"form": form, "msg": msg})
        return render(request, "login.html", {"form": form, "msg": msg, "is_ok": True})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

@login_required(login_url='/login')
def user_list_view(request):
    page = int(request.GET.get("p", 1))
    users = Users.objects.all().order_by("-id")
    paginator = Paginator(users, 10)
    users = paginator.get_page(page)

    return render(request, "users.html", {"users": users})