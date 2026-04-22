from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import DeathCertificate, Deceased, Certifiers
from .serializer import CertifiersSerializer, DeathCertificateSerializer, DeceasedSerializer

class DeceasedViewSet(ModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer

class CertifiersViewSet(ModelViewSet):
    queryset = Certifiers.objects.all()
    serializer_class = CertifiersSerializer

class DeathCertificateViewSet(ModelViewSet):
    queryset = DeathCertificate.objects.all()
    serializer_class = DeathCertificateSerializer

# class DeathRecordViewSet(ModelViewSet):
#     queryset = DeathRecords.objects.all()
#     serializer_class = DeathRecordSerializer
