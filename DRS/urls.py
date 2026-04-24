from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSets
from records.views import BurialDetailsViewSet, DeathCertificateViewSet, DeathRecordViewSet, DeceasedNextOfKinViewSet, DeceasedViewSet, CertifiersViewSet, FuneralHomeViewSet, MedicalInstitutionViewSet, NextOfKinViewSet, DeceasedFuneralHomeViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register(r'users', UserViewSets)
router.register(r'deceased', DeceasedViewSet)
router.register(r'certifiers', CertifiersViewSet)
router.register(r'death-certificates', DeathCertificateViewSet)
router.register(r'next-of-kin', NextOfKinViewSet)
router.register(r'medical-institutions', MedicalInstitutionViewSet)
router.register(r'funeral-homes', FuneralHomeViewSet)
router.register(r'deceased-funeral-homes', DeceasedFuneralHomeViewSet)
router.register(r'deceased-next-of-kin', DeceasedNextOfKinViewSet)
router.register(r'death-records', DeathRecordViewSet)
router.register(r'burial-details', BurialDetailsViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]