from django.contrib import admin

from records.models import Certifiers, DeathCertificate, Deceased, DeceasedFuneralHome, DeceasedFuneralHome, FuneralHome, MedicalInstitution, NextOfKin

admin.site.register(Deceased)
admin.site.register(Certifiers)
admin.site.register(DeathCertificate)
admin.site.register(NextOfKin)
admin.site.register(MedicalInstitution)
admin.site.register(FuneralHome)
admin.site.register(DeceasedFuneralHome)