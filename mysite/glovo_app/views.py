from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['store_name']


class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner]


class StoreOwnerListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [CheckOwner]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckOwnerEdit, CheckOwner]


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CheckOwner]


class ProductOwnerListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    permission_classes = [CheckOwner]

    def get_queryset(self):
        return Product.objects.filter(store__owner=self.request.user)


class ProductOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CheckOwnerProductEdit, CheckOwner]


class ComboCreateAPIView(generics.CreateAPIView):
    serializer_class = ComboSerializer
    permission_classes = [CheckOwner]


class ComboOwnerListAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboListSerializer
    permission_classes = [CheckOwner]

    def get_queryset(self):
        return Combo.objects.filter(store__owner=self.request.user)


class ComboOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        return CartProduct.objects.filter(cart__user=self.request.user)


class CartComboViewSet(viewsets.ModelViewSet):
    queryset = CartCombo.objects.all()
    serializer_class = CartComboSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        return CartCombo.objects.filter(cart__user=self.request.user)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [CheckClient]


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CheckUser]


class CourierAPIView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [CheckCourier]

    def get_queryset(self):
        return Courier.objects.filter(user=self.request.user)


class CourierEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [CheckUser, CheckCourier]


class CourierOrderAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CheckCourier]

    def get_queryset(self):
        return Order.objects.filter(courier=self.request.user)


class StoreReviewAPIView(generics.CreateAPIView):
    serializer_class = StoreReviewCreateSerializer
    permission_classes = [CheckClient]


class CourierRatingAPIView(generics.CreateAPIView):
    serializer_class = CourierRatingSerializer
    permission_classes = [CheckClient]
