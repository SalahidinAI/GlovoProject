from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user_list')
router.register(r'category', CategoryViewSet, basename='category_list')
router.register(r'store', StoreViewSet, basename='store_list')
router.register(r'product', ProductViewSet, basename='_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')
# router.register(r'store', StoreViewSet, basename='store_list')

urlpatterns = [
    path('', include(router.urls)),
]