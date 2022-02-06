from django.contrib import admin
from kep.models import JenisBarang, Barang, NomorSkep

# Register your models here.

admin.site.register(NomorSkep)
admin.site.register(JenisBarang)
admin.site.register(Barang)
