from django.contrib import admin

from .models import Consultation, UploadedFile


class UploadedFileAdmin(admin.StackedInline):
    model = UploadedFile
    extra = 1               # extra empty upload fields


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    inlines = [UploadedFileAdmin]

    class Meta:
        model = Consultation


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    pass
