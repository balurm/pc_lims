from django.contrib import admin
from .models import Buffer, Precipitant, Additive, Reservoirsolution, Protein, Plate, Cell, Observation

class BufferAdmin(admin.ModelAdmin):
  list_display = ("name", "make", "addedby", "makedate",)

class PrecipAdmin(admin.ModelAdmin):
  list_display = ("name", "make", "makedate",)

class AdditiveAdmin(admin.ModelAdmin):
  list_display = ("name", "make", "makedate",)

class ReservoirAdmin(admin.ModelAdmin):
  list_display = ("rs_combinedname", "buffer", "precipitant",)

# Register your models here.
admin.site.register(Buffer, BufferAdmin)
admin.site.register(Precipitant, PrecipAdmin)
admin.site.register(Additive, AdditiveAdmin)
admin.site.register(Reservoirsolution, ReservoirAdmin)

admin.site.register(Protein)
admin.site.register(Plate)
admin.site.register(Cell)
admin.site.register(Observation)

