from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("account", views.account_view, name="account"),
    path("order", views.order_view, name="order"),
    path("menu", views.menu_view, name="menu"),
    path("update", views.update, name="update"),
    path("add", views.add, name="add"),
    path("remove/<item>", views.remove, name="remove"),
    path("place", views.place, name="place"),
    path("success", views.success_view, name="success")
]