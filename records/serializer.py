from rest_framework import serializers
import rest_framework
from .models import Certifiers, DeathRecords, Deceased , DeathCertificate, DeceasedFuneralHome, DeceasedNextOfKin, FuneralHome, MedicalInstitution, NextOfKin
from datetime import date

class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = "__all__"
        def create(self, validated_data):
            month = validated_data.pop("month")
            year = validated_data.pop("year")

            validated_data["date_of_birth"] = date(year, month, 1)
            return super().create(validated_data)

class CertifiersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certifiers
        fields = "__all__"

class DeathCertificateSerializer(serializers.ModelSerializer):
    month = serializers.IntegerField(write_only=True)
    year = serializers.IntegerField(write_only=True)

    class Meta:
        model = DeathCertificate
        fields =   fields = [
            "id",
            "deceased",
            "certificate_number",
            "date_of_death",
            "other_findings",
            "place_of_death",
            "cause_of_death",
            "date_issued",
            "status",
            "date_registered",
            "month",
            "year",
        ]
        read_only_fields = ["certifier", "status", "date_registered", "certificate_number"]

    def create(self, validated_data):
        request = self.context['request']

        # extract custom fields
        month = validated_data.pop("month")
        year = validated_data.pop("year")

        # build date
        validated_data["date_of_death"] = date(year, month, 1)

        # assign logged-in user
        validated_data["certifier"] = request.user

        return super().create(validated_data)

class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = "__all__"

class MedicalInstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalInstitution
        fields = "__all__"

    def validate(self, data):
        institution_type = data.get("institution_type")
        other_name = data.get("other_institution_name")

        if institution_type == "Other" and not other_name:
            raise serializers.ValidationError({
                "other_institution_name": "This field is required when institution type is 'Other'."
            })
    
        return data
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        return obj.display_name()

class FuneralHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuneralHome
        fields = "__all__"  

class DeceasedFuneralHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeceasedFuneralHome
        fields = "__all__"

class DeceasedNextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeceasedNextOfKin
        fields = "__all__"

class DeathRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeathRecords
        fields = "__all__"
    
        read_only_fields = ["certifier", "status", "date_registered"]

    def create(self, validated_data):
        month = validated_data.pop("month")
        year = validated_data.pop("year")

        validated_data["date_of_death"] = date(year, month, 1)
        return super().create(validated_data)