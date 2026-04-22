from django.contrib.auth.models import Group

def create_user_groups():
    Group.objects.get_or_create(name="Certifier")
    Group.objects.get_or_create(name="Admin")
    Group.objects.get_or_create(name="Clerk")