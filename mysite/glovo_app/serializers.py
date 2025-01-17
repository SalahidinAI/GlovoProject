from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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


class CartComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartCombo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


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


class CourierRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierRating
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_store = StoreListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_store']


# I'm fulling this class with combo, products ...
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
