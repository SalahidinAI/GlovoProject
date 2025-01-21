from rest_framework import serializers
from .models import (User, Category, Store, StoreContact, StoreWebsite, StoreAddress, Product,
                     Combo, Cart, CartProduct, CartCombo, Order, Courier, CourierRating, StoreReview)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'user_image', 'first_name', 'last_name',
                  'age','email', 'phone_number', 'password', 'role', 'data_register')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_image', 'role', 'age', 'email', 'phone_number',
                  'password', 'data_register']


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role']


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class StoreListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()
    good_star = serializers.SerializerMethodField()
    category = CategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'store_image', 'category', 'avg_rating', 'count_rating', 'good_star']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()

    def get_good_star(self, obj):
        return obj.get_good_star()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreContact
        fields = ['title', 'contact']


class StoreWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreWebsite
        fields = ['website_name', 'website']


class StoreAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAddress
        fields = ['address']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_image', 'description', 'price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ComboListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ['id', 'combo_name', 'combo_image', 'description', 'price']


class ComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'


class CartProductSimpleSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']


class CartComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartCombo
        fields = '__all__'


class CartComboSimpleSerializer(serializers.ModelSerializer):
    combo = ComboListSerializer()

    class Meta:
        model = CartCombo
        fields = ['combo', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    cart_product = CartProductSimpleSerializer()
    cart_combo = CartComboSimpleSerializer()
    courier = UserNameSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    products_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart_product', 'cart_combo', 'delivery_address',
                  'status', 'products_total_price', 'courier', 'created_at']

    def get_products_total_price(self, obj):
        return obj.get_products_total_price()


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    user = UserNameSerializer()
    courier = UserNameSerializer()
    cart_product = CartProductSimpleSerializer()
    cart_combo = CartComboSimpleSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart_product', 'cart_combo',
                  'delivery_address', 'status', 'courier', 'created_at']

    def validate(self, data):
        if not data.get('cart_product') and not data.get('cart_combo'):
            raise serializers.ValidationError({
                'cart_product': "You must select at least one of 'cart_product' or 'cart_combo'.",
                'cart_combo': "You must select at least one of 'cart_product' or 'cart_combo'."
            })
        return data


class CourierSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Courier
        fields = ['id', 'user', 'status', 'current_orders', 'avg_rating', 'count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class StoreReviewSerializer(serializers.ModelSerializer):
    client = UserNameSerializer()
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))

    class Meta:
        model = StoreReview
        fields = ['client', 'comment', 'star', 'created_date']


class StoreReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = '__all__'

    def validate(self, data):
        if not data.get('comment') and not data.get('star'):
            raise serializers.ValidationError({
                'comment': "You have to choose one of these comment or star.",
                'star': "You have to choose one of these comment or star."
            })
        return data


class CourierRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierRating
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_store = StoreListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_store']


class StoreDetailSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer()
    category = CategoryListSerializer(many=True, read_only=True)
    store_address = StoreAddressSerializer(many=True, read_only=True)
    store_contact = StoreContactSerializer(many=True, read_only=True)
    store_website = StoreWebsiteSerializer(many=True, read_only=True)
    store_product = ProductListSerializer(many=True, read_only=True)
    store_combo = ComboListSerializer(many=True, read_only=True)
    store_review = StoreReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'category', 'description', 'owner',
                  'store_address', 'store_contact', 'store_website',
                  'store_product', 'store_combo', 'store_review']
