from rest_framework import serializers
from .models import Sale, Customer, Product, Tag

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'phone_number', 'gender', 'age', 'region', 'customer_type']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'brand', 'category', 'tags']

class SaleSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = [
            'transaction_id','date','customer','product','quantity','price_per_unit',
            'discount_percentage','total_amount','final_amount','payment_method',
            'order_status','delivery_type','store_id','store_location','salesperson_id','employee_name'
        ]
