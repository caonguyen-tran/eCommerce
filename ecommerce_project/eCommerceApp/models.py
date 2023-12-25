from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/user_avatar/%y/%m')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)


class Role(models.Model):
    name = models.CharField(max_length=50, null=False)


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    price = models.FloatField(null=False)
    description = RichTextField
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


class Review(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    update_create = models.DateTimeField(auto_now=True)
    comment = RichTextField()
    rate = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class ReviewProduct(Review):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)


class ReviewSeller(Review):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Shop(models.Model):
    name = models.CharField(max_length=200, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    confirm_status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField()


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    coupon = models.FloatField()
    ship_fee = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        ordering = ['id']


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField()

    class Meta:
        ordering = ['order']
