
from django.contrib import admin
from django.urls import path

from usermanager.views import index, login_view, logout_view, user_list_view, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("users", user_list_view, name="user_list_view"),
    path("register", register, name="register"),
]
