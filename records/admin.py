from django.contrib import admin

from records.models import Certifiers, DeathCertificate, Deceased

admin.site.register(Deceased)
admin.site.register(Certifiers)
admin.site.register(DeathCertificate)