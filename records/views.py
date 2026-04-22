from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import  BurialDetails, Certifiers, DeathCertificate, DeathRecords, Deceased, DeceasedFuneralHome, DeceasedNextOfKin, FuneralHome, MedicalInstitution, NextOfKin
from .serializer import BurialDetailsSerializer, DeathCertificateSerializer, DeathRecordSerializer, DeceasedFuneralHomeSerializer, DeceasedNextOfKinSerializer, DeceasedSerializer,CertifiersSerializer, FuneralHomeSerializer, MedicalInstitutionSerializer, NextOfKinSerializer

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

    def get_queryset(self):
        queryset = DeceasedNextOfKin.objects.all()

        next_of_kin_id = self.request.query_params.get('next_of_kin')

        if next_of_kin_id:
            queryset = queryset.filter(next_of_kin_id=next_of_kin_id)

        return queryset
class DeathRecordViewSet(ModelViewSet):
    queryset = DeathRecords.objects.all()
    serializer_class = DeathRecordSerializer

class BurialDetailsViewSet(ModelViewSet):
    queryset = BurialDetails.objects.all()
    serializer_class = BurialDetailsSerializer
