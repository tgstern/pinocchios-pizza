from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Sum
from .models import *

# index view
def index(request):
    return render(request, "orders/index.html")

# login view
def login_view(request):
    if request.method == "GET":
        return render(request, "orders/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("menu"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})
    
# register view
def register_view(request):
    if request.method == "GET":
        return render(request, "orders/register.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        first = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        if (username == '') or (password == '') or (first == '') or (last == '') or (email == ''):
            return render(request, "orders/register.html", {"message": "Registration Error. Please re-enter information."})
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first, last_name=last)
        except:
            return render(request, "orders/register.html", {"message": "User already exists. Please try a different username and/or email address."})
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("menu"))
        else:
            return render(request, "orders/register.html", {"message": "Registration Error. Please re-enter information."})
        
# logout view
def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

# menu view
def menu_view(request):
    if request.user.is_authenticated:
        message = None
    else:
        message = "Please log in to place an order."
    context = {
            "pizzas": MenuItem.objects.filter(category="pi"),
            "spizzas": MenuItem.objects.filter(category="si"),
            "toppings": Topping.objects.all(),
            "subs": MenuItem.objects.filter(category="su"),
            "platters": MenuItem.objects.filter(category="di"),
            "pastasalads": MenuItem.objects.filter(category="pa"),
            "message": message
        }
    return render(request, "orders/menu.html", context)

# add function
def add(request):
    if request.user.is_authenticated:
        itemid = str(request.POST.get("id"))
        item = MenuItem.objects.get(id=itemid)
        if request.POST.get(itemid) == None:
            size = 'Small'
            price = item.sprice
        elif request.POST.get(itemid) == "Large":
            size = 'Large'
            price = item.lprice
        tops = request.POST.getlist("top"+itemid)
        order = LineItem.objects.create(customer=request.user, item=item, size=size, price=price)
        order.toppings.set(tops)
        return HttpResponseRedirect(reverse("menu"))
    else:
        return HttpResponseRedirect(reverse("menu"))

# remove function
def remove(request, item):
    LineItem.objects.get(id=item).delete()
    return HttpResponseRedirect(reverse("order"))
    
# cart view
@login_required
def order_view(request):
    context = {
        "items": LineItem.objects.filter(customer=request.user.id, placed=False),
        "total": LineItem.objects.filter(customer=request.user.id, placed=False).aggregate(Sum("price"))["price__sum"]
    }
    return render(request, "orders/order.html", context)

# place order function
def place(request):
    total = float(request.POST.get("total"))
    tip = request.POST.get("tip")
    if tip != "":
        total += float(tip)
    total = round(total, 2)
    items = LineItem.objects.filter(customer=request.user.id, placed=False)
    order = Order.objects.create(customer=request.user, total=total)
    order.items.set(items)
    items.update(placed=True)
    return HttpResponseRedirect(reverse("success"))

# order successfully placed view
def success_view(request):
    return render(request, "orders/success.html")

# account view
@login_required
def account_view(request):
    context = {
        "orders": Order.objects.filter(customer=request.user.id).order_by('-date')
    }
    return render(request, "orders/account.html", context)

# update function
@login_required
def update(request):
    user = request.user
    first = request.POST["first"]
    last = request.POST["last"]
    if first != '':
        user.first_name = first
    if last != '':
        user.last_name = last
    user.save()
    return HttpResponseRedirect(reverse("account"))
