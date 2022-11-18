from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from money_manager.views import ProfileViewSet, TransactionViewSet, CategoryViewSet, RegistrationViewSet


router = routers.DefaultRouter()
router.register('transaction', TransactionViewSet, basename='Transaction')
router.register(r'category', CategoryViewSet, basename='Category')
router.register(r'profile', ProfileViewSet, basename='Profile')
router.register(r'registration', RegistrationViewSet, basename='Registration')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/v1/', include(router.urls)),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
