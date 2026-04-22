from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSets
from records.views import  DeceasedFuneralHomeViewSet, DeceasedNextOfKinViewSet, DeceasedViewSet, CertifiersViewSet, DeathCertificateViewSet, FuneralHomeViewSet, MedicalInstitutionViewSet, NextOfKinViewSet

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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]