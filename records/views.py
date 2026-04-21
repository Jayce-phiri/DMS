from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Deceased
from .serializer import DeceasedSerializer

class DeceasedViewSet(ModelViewSet):
    queryset = Deceased.objects.all()
    serializer_class = DeceasedSerializer


