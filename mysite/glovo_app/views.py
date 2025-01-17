from rest_framework import viewsets, generics
from .models import *
from .serializers import *


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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ComboViewSet(viewsets.ModelViewSet):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


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


class StoreReviewViewSet(viewsets.ModelViewSet):
    queryset = StoreReview.objects.all()
    serializer_class = StoreReviewSerializer


class CourierRatingViewSet(viewsets.ModelViewSet):
    queryset = CourierRating.objects.all()
    serializer_class = CourierRatingSerializer
