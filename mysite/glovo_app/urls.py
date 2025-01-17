from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user_list')
router.register(r'product', ProductViewSet, basename='_list')


urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('store/create/', StoreCreateAPIView.as_view(), name = 'store_create'),
    path('review/', StoreReviewViewSet.as_view({'get': 'list'}), name = 'review'),
    path('courier_rating/', CourierRatingViewSet.as_view({'get': 'list'}), name = 'courier_rating')
]