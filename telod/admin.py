from django.contrib import admin
from telod.models import Medicine, MedicineName


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    ordering = ["main_name"]


@admin.register(MedicineName)
class MedicineAdmin(admin.ModelAdmin):
    ordering = ["name"]
