from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'major', 'study_type', 'status', 'created_at')
    list_filter = ('status', 'study_type', 'created_at')
    search_fields = ('full_name', 'passport_number', 'major', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Applicant Information', {
            'fields': ('user', 'full_name', 'passport_number', 'major', 'study_type')
        }),
        ('Required Documents', {
            'fields': (
                'cover_letter', 'cv', 'passport_file', 'personal_image',
                'highest_degree', 'transcript', 'recommendation_letter1', 
                'recommendation_letter2', 'english_proficiency', 'medical_exam',
                'conduct_certificate', 'intro_video'
            )
        }),
        ('Optional Documents', {
            'fields': ('research_proposal', 'additional_certificates', 'other_files'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )