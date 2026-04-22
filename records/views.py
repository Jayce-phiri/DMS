from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import DeathCertificate, Deceased, Certifiers, DeceasedFuneralHome, FuneralHome, MedicalInstitution, NextOfKin, DeceasedNextOfKin, DeathRecords
from .serializer import CertifiersSerializer, DeathCertificateSerializer, DeceasedSerializer, NextOfKinSerializer, FuneralHomeSerializer, MedicalInstitutionSerializer, NextOfKinSerializer, DeceasedFuneralHomeSerializer, DeceasedNextOfKinSerializer, DeathRecordSerializer

class DeceasedViewSet(ModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer

class CertifiersViewSet(ModelViewSet):
    queryset = Certifiers.objects.all()
    serializer_class = CertifiersSerializer

class DeathCertificateViewSet(ModelViewSet):
    queryset = DeathCertificate.objects.all()
    serializer_class = DeathCertificateSerializer

class NextOfKinViewSet(ModelViewSet):
    queryset = NextOfKin.objects.all()
    serializer_class = NextOfKinSerializer

class MedicalInstitutionViewSet(ModelViewSet):
    queryset = MedicalInstitution.objects.all()
    serializer_class = MedicalInstitutionSerializer

class FuneralHomeViewSet(ModelViewSet):
    queryset = FuneralHome.objects.all()
    serializer_class = FuneralHomeSerializer

class DeceasedFuneralHomeViewSet(ModelViewSet):
    queryset = DeceasedFuneralHome.objects.all()
    serializer_class = DeceasedFuneralHomeSerializer

class DeceasedNextOfKinViewSet(ModelViewSet):
    queryset = DeceasedNextOfKin.objects.all()
    serializer_class = DeceasedNextOfKinSerializer

class DeathRecordViewSet(ModelViewSet):
    queryset = DeathRecords.objects.all()
    serializer_class = DeathRecordSerializer


