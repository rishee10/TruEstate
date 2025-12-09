from django.db import models

# Create your models here.

from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=32, db_index=True)
    gender = models.CharField(max_length=32, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    region = models.CharField(max_length=128, blank=True, null=True)
    customer_type = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['region']),
        ]




class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=128, blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['category']),
        ]


class Sale(models.Model):
    transaction_id = models.CharField(max_length=64, unique=True)
    date = models.DateField(db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=64)
    order_status = models.CharField(max_length=64)
    delivery_type = models.CharField(max_length=64)
    store_id = models.CharField(max_length=64)
    store_location = models.CharField(max_length=128)
    salesperson_id = models.CharField(max_length=64)
    employee_name = models.CharField(max_length=128)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['payment_method']),
        ]
