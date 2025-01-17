from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user_list')


urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('review/', StoreReviewAPIView.as_view(), name='review_list'),
    path('rating/', CourierRatingAPIView.as_view(), name='rating_list'),
    path('store_list/', StoreOwnerListAPIVeiw.as_view(), name='store_owner_list'),
    path('store_list/<int:pk>/', StoreOwnerEditAPIView.as_view(), name='store_owner_edit'),
    path('store/create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('product/', ProductOwnerListAPIView.as_view(), name='product_owner_list'),
    path('product/<int:pk>/', ProductOwnerEditAPIView.as_view(), name='product_owner_edit'),
    path('product/create/', ProductCreateAPIView.as_view(), name='product_owner_create'),
    path('combo/', ComboOwnerListAPIView.as_view(), name='combo_owner_list'),
    path('combo/<int:pk>/', ComboOwnerEditAPIView.as_view(), name='combo_owner_edit'),
    path('combo/create/', ComboCreateAPIView.as_view(), name='combo_owner_create'),
]
