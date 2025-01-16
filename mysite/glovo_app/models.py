from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='age', null=True, blank=True,
                                           validators=[MinValueValidator(18), MaxValueValidator(80)])
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    data_register = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ROLE_CHOICES = (
        ('client', 'client'),
        ('courier', 'courier'),
        ('owner', 'owner'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=16, default='client')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'user'
        permissions = [

        ]


class Store(models.Model):
    store_name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    contact_info = models.TextField()
    address = models.CharField(max_length=120, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_name}, {self.address}'


class Product(models.Model):
    product_name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    combo = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product_name}, {self.price}'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders')
    products = models.ManyToManyField(Product)
    ORDER_STATUS = (
        ('waiting for processing', "waiting for processing"),
        ('In the process of delivery', 'In the process of delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    )
    status = models.CharField(choices=ORDER_STATUS, max_length=100)
    delivery_address = models.CharField(max_length=120, blank=True)
    courier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.client}, {self.products}, {self.status}, {self.courier}'


class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    COURIER_STATUS = (
        ('busy', 'busy'),
        ('available', 'available')
    )
    status = models.CharField(choices=COURIER_STATUS, max_length=50)
    current_orders = models.ManyToManyField(Order, blank=True, related_name='assigned_couriers')

    def __str__(self):
        return f'{self.user}'


class StoreReview(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    comment = models.CharField(max_length=500)

class CourierRating(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
