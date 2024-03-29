import cloudinary.api
from rest_framework import serializers
from .models import Category, Product, Shop, User, CartDetail, Order, OrderDetail, Pay
from cloudinary import CloudinaryResource


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone', 'address', 'is_active',
                  'date_joined',
                  'avatar', 'is_admin', 'is_buyer', 'is_seller', 'is_employee']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(user.password)
        user.is_buyer = True
        user.is_seller = False
        user.is_employee = False
        user.is_admin = False
        user.is_active = True
        user.save()

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ShopSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'date_created', 'logo', 'confirm_status', 'user']


class ProductSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'shop', 'category']


class CartDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserSerializer()

    class Meta:
        model = CartDetail
        fields = ['id', 'product', 'quantity', 'total_price', 'user']


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['id', 'name', 'image']


class OrderSerializer(serializers.ModelSerializer):
    pay = PaySerializer()

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'address', 'total_price', 'user', 'pay']


class OrderDetailSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ['id', 'quantity', 'total_price', 'order', 'product']
