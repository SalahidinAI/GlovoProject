from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user_list')
router.register(r'cart', CartViewSet, basename='cart_list')
router.register(r'cart_product', CartProductViewSet, basename='cart_product_list')
router.register(r'cart_combo', CartComboViewSet, basename='cart_combo_product_list')
# router.register(r'courier', CourierViewSet, basename='courier_list')


urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('review/', StoreReviewAPIView.as_view(), name='store_review_list'),
    path('rating/', CourierRatingAPIView.as_view(), name='courier_rating_list'),
    path('store_list/', StoreOwnerListAPIView.as_view(), name='store_owner_list'),
    path('store_list/<int:pk>/', StoreOwnerEditAPIView.as_view(), name='store_owner_edit'),
    path('store/create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('product/', ProductOwnerListAPIView.as_view(), name='product_owner_list'),
    path('product/<int:pk>/', ProductOwnerEditAPIView.as_view(), name='product_owner_edit'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_owner_create'),
    path('combo/', ComboOwnerListAPIView.as_view(), name='combo_owner_list'),
    path('combo/<int:pk>/', ComboOwnerEditAPIView.as_view(), name='combo_owner_edit'),
    path('combo/create/', ComboCreateAPIView.as_view(), name='combo_owner_create'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order_create'),
    path('order/', OrderListAPIView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('courier/', CourierAPIView.as_view(), name='courier_list'),
    path('courier/<int:pk>/', CourierEditAPIView.as_view(), name='courier_list'),
    path('courier/order/', CourierOrderAPIView.as_view(), name='courier_order_list'),
]
