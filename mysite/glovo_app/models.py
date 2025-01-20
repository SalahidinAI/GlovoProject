from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator


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


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Store(models.Model):
    category = models.ManyToManyField(Category, related_name='category_store')
    store_image = models.ImageField(upload_to='store_image')
    store_name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_name}'

    def get_reviews_data(self):
        all_reviews = self.store_review.all()
        total_stars = [i.star for i in all_reviews if i.star]
        return total_stars

    def get_avg_rating(self):
        total_stars = self.get_reviews_data()
        if total_stars:
            return round(sum(total_stars) / len(total_stars), 1)
        return 0

    def get_count_rating(self):
        total_stars = self.get_reviews_data()
        count_stars = len(total_stars)
        count_rating = count_stars if count_stars < 3 else '3+'
        if count_rating:
            return count_rating
        return 0

    def get_good_star(self):
        total_stars = self.get_reviews_data()
        good_stars = [i for i in total_stars if i >=4]
        if total_stars:
            percent = round(100 / len(total_stars) * len(good_stars), 1)
            return f'{percent}%'
        return '0%'

    # def get_avg_rating(self):
    #     reviews = self.store_review.all()
    #     total_stars = [i.star for i in reviews if i.star]
    #     avg_star = round(sum(total_stars) / len(total_stars), 1)
    #     good_star = round(100 / len(total_stars) * len([i for i in total_stars if i >=4]), 1)
    #     count_rating = len(total_stars) if len(total_stars) < 3 else '3+'
    #     if reviews.exists():
    #         return avg_star, count_rating, f'{good_star}%'
    #     return 0



class StoreContact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_contact')
    title = models.CharField(max_length=32, null=True, blank=True)
    contact = PhoneNumberField()

    class Meta:
        unique_together = ('store', 'contact')

    def __str__(self):
        return f'{self.store} {self.store}'


class StoreWebsite(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_website')
    WEBSITE_CHOICES = (
        ('Instagram', 'Instagram'),
        ('Telegram', 'Telegram'),
        ('Linkedin', 'Linkedin'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
    )
    website_name = models.CharField(choices=WEBSITE_CHOICES, max_length=32)
    website = models.URLField()

    def __str__(self):
        return f'{self.store} {self.website}'


class StoreAddress(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_address')
    address = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.store} {self.address}'


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product')
    product_name = models.CharField(max_length=60, unique=True)
    product_image = models.ImageField(upload_to='product_image/', null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product_name}, {self.price}'


class Combo(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_combo')
    combo_name = models.CharField(max_length=64)
    combo_image = models.ImageField(upload_to='combo_image')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.combo_name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_product')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders')
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
        return f'{self.user}, {self.cart_product}, {self.cart_combo} {self.status}, {self.courier}'

    def clean(self):
        super().clean()
        if not self.cart_product and not self.cart_combo:
            raise ValidationError("You must select at least one of 'cart_product' or 'cart_combo'.")


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
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_review')
    star = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.client} {self.store}'

    def clean(self):
        super().clean()
        if not self.star and not self.comment:
            raise ValidationError('You have to choose one of these comment or star')


class CourierRating(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.client} {self.courier}'
