from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=2000, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    feature_1 = models.CharField(max_length=510, null=True, blank=True)
    feature_2 = models.CharField(max_length=510, null=True, blank=True)
    feature_3 = models.CharField(max_length=510, null=True, blank=True)
    feature_4 = models.CharField(max_length=510, null=True, blank=True)
    feature_5 = models.CharField(max_length=510, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.user.username



class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(null=True, max_length=510)
    shipping_price = models.IntegerField(null=True, blank=True, default=0)
    is_through_buy_now_button = models.BooleanField(default=False)

    @property
    def total_cart_items(self):
        order_items = self.orderitem_set.all()
        total = 0
        for item in order_items:
            total += item.quantity

        return total

    @property
    def total_cart_price(self):
        order_items = self.orderitem_set.all()
        total = 0
        for item in order_items:
            total += item.total_price

        return total

    @property
    def total_cart_price_with_shipping_price(self):
        return self.total_cart_price + self.shipping_price

    def __str__(self):
        return f"{self.customer}-{self.id}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL , null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE , null=True, blank=True)
    address = models.TextField(max_length=1000, null=True)
    optional_address = models.TextField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.address
