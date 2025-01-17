from rest_framework import viewsets, generics
from .models import *
from .serializers import *
from .permissions import *


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


# proses
class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner]


class StoreOwnerListAPIVeiw(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [CheckOwner]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)


class StoreOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckOwnerStoreEdit, CheckOwner]


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CheckOwner]


class ProductOwnerListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
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
    permission_classes = [CheckOwnerProductEdit, CheckOwner]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer


class CartComboViewSet(viewsets.ModelViewSet):
    queryset = CartCombo.objects.all()
    serializer_class = CartComboSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class StoreReviewAPIView(generics.CreateAPIView):
    serializer_class = StoreReviewCreateSerializer
    permission_classes = [CheckClient]


class CourierRatingAPIView(generics.CreateAPIView):
    serializer_class = CourierRatingSerializer
    permission_classes = [CheckClient]
