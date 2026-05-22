from rest_framework import request
from rest_framework.viewsets import ModelViewSet
from .models import User
from accounts.serializers import UserSerializer
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def members(request):
    users = User.objects.all()
    template = loader.get_template('members.html')
    context ={
        'users': users
    }
    return HttpResponse(template.render(context, request))

def member_details(request, id):
    user = User.objects.get(id=id)
    template = loader.get_template('member_details.html')
    context ={
        'user': user
    }
    return HttpResponse(template.render(context, request))

def dashboard(request):
    return render(request, 'Dashboard.html')

def home(request):
   
    return render(request, 'Home.html')