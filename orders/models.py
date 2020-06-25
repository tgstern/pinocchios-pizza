from django.db import models
from django.contrib.auth.models import User

# user validation specification
User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True

# menu item model for all items
class MenuItem(models.Model):
    CATEGORIES = [
        ("pi", "Pizza"),
        ("si", "Sicilian"),
        ("su", "Subs"),
        ("pa", "Pasta and Salad"),
        ("di", "Dinner Platter")
    ]
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    toppings = models.IntegerField(null=True)
    sprice = models.DecimalField(max_digits=4, decimal_places=2)
    lprice = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return self.name

# listing of available pizza toppings
class Topping(models.Model):
    topping = models.CharField(max_length=32)
    def __str__(self):
        return self.topping

# list of line items added to cart
class LineItem(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)
    toppings = models.ManyToManyField(Topping, blank=True)
    size = models.CharField(max_length=5, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    placed = models.BooleanField(default=False)
    def __str__(self):
        return self.item.name + " - "+ self.customer.username

# list of relational orders
class Order(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    items = models.ManyToManyField(LineItem)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return self.customer.username + "-" + str(self.total) + "-" + str(self.date)
