from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSets
from records.views import DeceasedViewSet

router = DefaultRouter()
router.register(r'users', UserViewSets)
router.register(r'deceased', DeceasedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]