from email.mime import text
import uuid
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import action
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
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

class CanApproveDeathRecord(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("records.can_approve_deathrecord")
    

class DeathRecordViewSet(ModelViewSet):
    queryset = DeathRecords.objects.all()
    serializer_class = DeathRecordSerializer
    def get_permissions(self):
        if self.action in ["approve", "reject"]:
            permission_classes = [IsAuthenticated, CanApproveDeathRecord]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        record = self.get_object()

        record.status = "APPROVED"
        record.save()

        # 🔥 SEND REAL-TIME NOTIFICATION
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"{record.deceased.title_and_name} has been approved"
            }
        )

        return Response({"message": "Approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        record = self.get_object()

        if record.status == "APPROVED":
            return Response({"error": "Cannot reject an approved record"}, status=400)

        record.status = "REJECTED"
        record.is_locked = True
        record.save()

        return Response({"message": "Record rejected"})
    
    def update(self, request, *args, **kwargs):
        record = self.get_object()

        if record.is_locked:
            return Response(
                {"error": "This record is locked and cannot be edited"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def certificate(self, request, pk=None):
        record = self.get_object()
        deceased = record.deceased
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="death_certificate_{record.certificate_number}.pdf"'

        c = canvas.Canvas(response)

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(300, 800, "OFFICIAL DEATH CERTIFICATE")

        c.setFont("Helvetica", 12)

        # Start text block
        text = c.beginText(80, 750)
        text.setFont("Helvetica", 12)

        # Deceased info
        text.textLine(f"Full Name: {record.deceased.title_and_name}")
        text.textLine(f"Date of Death: {record.date_of_death}")
        text.textLine(f"Place of Death: {record.place_of_death}")
        text.textLine(f"Cause of Death: {record.cause_of_death}")

        # Extra details
        if record.other_findings:
            text.textLine(f"Other Findings: {record.other_findings}")

        text.textLine(f"Certificate Number: {record.certificate_number}")
        text.textLine(f"Date Issued: {record.date_issued}")
        text.textLine(f"Date Registered: {record.date_registered}")

        # Certifier
        certifier_name = record.certifier.full_name if record.certifier else "N/A"
        text.textLine(f"Certified By: {certifier_name}")

        c.drawText(text)

        c.showPage()
        c.save()

        return response


class BurialDetailsViewSet(ModelViewSet):
    queryset = BurialDetails.objects.all()
    serializer_class = BurialDetailsSerializer


    