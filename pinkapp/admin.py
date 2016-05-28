from django.contrib import admin
from .models import marca, perfume

# Register your models here.
class PerfumesAdmin(admin.TabularInline):
	model = perfume

@admin.register(marca)
class marcaAdmin(admin.ModelAdmin):
	inlines = (PerfumesAdmin,)
	list_display = ['__unicode__','nombre','imagen']

@admin.register(perfume)
class perfumeAdmin(admin.ModelAdmin):
	list_display = ['__unicode__','nombre','marca','precio','presentacion']


