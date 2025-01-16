from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# from multiselectfield import MultiSelectField


class User(AbstractUser):
    user_image = models.ImageField(upload_to='user_image', null=True, blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='age', null=True, blank=True,
                                           validators=[MinValueValidator(18), MaxValueValidator(80)])
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    data_register = models.DateTimeField(auto_now_add=True)
    ROLE_CHOICES = (
        ('client', 'client'),
        ('courier', 'courier'),
        ('owner', 'owner'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=16, default='client')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Store(models.Model):
    store_image = models.ImageField(upload_to='store_image')
    store_name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_name}'


class StoreContact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    contact = PhoneNumberField()

    class Meta:
        unique_together = ('store', 'contact')

    def __str__(self):
        return f'{self.store} {self.store}'


class StoreWebsite(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    website = models.URLField()

    def __str__(self):
        return f'{self.store} {self.website}'


class StoreAddress(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.store} {self.address}'


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product_name}, {self.price}'


class Combo(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    combo_image = models.ImageField(upload_to='combo_image')
    combo_name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # class Meta:
    #     unique_together = ('store', 'combo_name')

    def __str__(self):
        return f'{self.combo_name}'


class ComboProduct(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.product_name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cart} {self.product}'


class CartCombo(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cart} {self.combo}'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders')
    cart_product = models.ForeignKey(CartProduct, on_delete=models.CASCADE, null=True, blank=True)
    cart_combo = models.ForeignKey(CartCombo, on_delete=models.CASCADE, null=True, blank=True)
    ORDER_STATUS = (
        ('waiting for processing', "waiting for processing"),
        ('In the process of delivery', 'In the process of delivery'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled')
    )
    status = models.CharField(choices=ORDER_STATUS, max_length=100)
    delivery_address = models.CharField(max_length=120)
    courier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.cart_product}, {self.cart_combo} {self.status}, {self.courier}'


class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    COURIER_STATUS = (
        ('busy', 'busy'),
        ('available', 'available')
    )
    status = models.CharField(choices=COURIER_STATUS, max_length=50, default='available')
    current_orders = models.ManyToManyField(Order, related_name='assigned_couriers')

    def __str__(self):
        return f'{self.user} {self.status}'


class StoreReview(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.client} {self.store}'


class CourierRating(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.client} {self.courier}'
