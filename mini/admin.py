from django.contrib import admin
from .models import Donor,Bank,Admin,Camp,CampReg

admin.site.register(Donor)
admin.site.register(Admin)
admin.site.register(Bank)
admin.site.register(Camp)
admin.site.register(CampReg)

