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
]