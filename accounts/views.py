from rest_framework.viewsets import ModelViewSet
from .models import User
from accounts.serializers import UserSerializer


class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer