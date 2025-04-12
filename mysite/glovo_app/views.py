from rest_framework import viewsets, generics, status
from .models import (User, Category, Store, Product, Combo, Cart, CartProduct, CartCombo, Order, Courier)
from .serializers import (RefreshToken, UserSerializer, LoginSerializer, UserProfileSerializer, CategoryListSerializer,
                          CategoryDetailSerializer, StoreListSerializer, StoreDetailSerializer, StoreSerializer,
                          ProductListSerializer,
                          ProductSerializer, ComboListSerializer, ComboSerializer, CartSerializer,
                          CartProductSerializer, CartComboSerializer,
                          OrderListSerializer, OrderSerializer, CourierSerializer, OrderUpdateSerializer,
                          OrderCreateSerializer, StoreReviewCreateSerializer, CourierRatingSerializer)
from .permissions import CheckClient, CheckOwner, CheckCourier, CheckOwnerEdit, CheckOwnerProductEdit, CheckUser, \
    CheckCourierOrder
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter
from .paginations import TwoObjectPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'detail': f'Неправильные данные {e}'}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Ошибка сервера {e}'}, status=500)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'detail': f'Ошибка сервера: {e}'}, status=500)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({'detail': 'Неправильный ключ'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Ошибка сервера: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        try:
            return User.objects.filter(id=self.request.user.id)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return User.objects.none()

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except serializers.ValidationError:
            return Response({'detail': 'Неправильное изменение данных'}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Ошибка сервера: {e}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = TwoObjectPagination


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['store_name']
    pagination_class = TwoObjectPagination


class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            store = serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'detail': f'Неправильные данные, {e}'}, status.HTTP_400_BAD_REQUEST)
        except NameError as e:
            return Response({'detail': f'Ошибка в коде {e}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'detail': f'Сервер не работает {e}'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class StoreOwnerListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [CheckOwner]
    pagination_class = TwoObjectPagination

    def get_queryset(self):
        try:
            return Store.objects.filter(owner=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Store.objects.none()


class StoreOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckOwnerEdit, CheckOwner]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = TwoObjectPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CheckOwner]


class ProductOwnerListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['product_name', 'price']
    permission_classes = [CheckOwner]
    pagination_class = TwoObjectPagination

    def get_queryset(self):
        try:
            return Product.objects.filter(store__owner=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Product.objects.none()


class ProductOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CheckOwnerProductEdit, CheckOwner]


class ComboListAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboListSerializer
    pagination_class = TwoObjectPagination


class ComboDetailAPIView(generics.RetrieveAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer


class ComboCreateAPIView(generics.CreateAPIView):
    serializer_class = ComboSerializer
    permission_classes = [CheckOwner]


class ComboOwnerListAPIView(generics.ListAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboListSerializer
    permission_classes = [CheckOwner]

    def get_queryset(self):
        try:
            return Combo.objects.filter(store__owner=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Combo.objects.none()


class ComboOwnerEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Combo.objects.all()
    serializer_class = ComboSerializer
    permission_classes = [CheckOwner, CheckOwnerProductEdit]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        try:
            return Cart.objects.filter(user=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Cart.objects.none()


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        try:
            return CartProduct.objects.filter(cart__user=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return CartProduct.objects.none()


class CartComboViewSet(viewsets.ModelViewSet):
    queryset = CartCombo.objects.all()
    serializer_class = CartComboSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        try:
            return CartCombo.objects.filter(cart__user=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return CartCombo.objects.none()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [CheckClient]

    def get_queryset(self):
        try:
            return Order.objects.filter(user=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Order.objects.none()


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [CheckClient]


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    permission_classes = [CheckUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderSerializer


class CourierAPIView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [CheckCourier]

    def get_queryset(self):
        try:
            return Courier.objects.filter(user=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Courier.objects.none()


class CourierEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [CheckUser, CheckCourier]


class CourierOrderAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CheckCourier]

    def get_queryset(self):
        try:
            return Order.objects.filter(courier=self.request.user)
        except Exception as e:
            print(f'Ошибка сервера: {e}')
            return Order.objects.none()


class CourierOrderEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [CheckCourier, CheckCourierOrder]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderSerializer


class StoreReviewAPIView(generics.CreateAPIView):
    serializer_class = StoreReviewCreateSerializer
    permission_classes = [CheckClient]


class CourierRatingAPIView(generics.CreateAPIView):
    serializer_class = CourierRatingSerializer
    permission_classes = [CheckClient]
