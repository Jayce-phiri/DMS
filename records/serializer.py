from rest_framework import serializers
from .models import Deceased

class DeceasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deceased
        fields = "__all__"