from django.db import models
from django.conf import settings


class Application(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=150)
    passport_number = models.CharField(max_length=50)
    major = models.CharField(max_length=150)
    study_type = models.CharField(max_length=50)

    # Required documents
    cover_letter = models.FileField(upload_to='uploads/')
    cv = models.FileField(upload_to='uploads/')
    passport_file = models.FileField(upload_to='uploads/')
    personal_image = models.ImageField(upload_to='uploads/')
    highest_degree = models.FileField(upload_to='uploads/')
    transcript = models.FileField(upload_to='uploads/')
    recommendation_letter1 = models.FileField(upload_to='uploads/')
    recommendation_letter2 = models.FileField(upload_to='uploads/')
    english_proficiency = models.FileField(upload_to='uploads/')
    medical_exam = models.FileField(upload_to='uploads/')
    conduct_certificate = models.FileField(upload_to='uploads/')
    intro_video = models.FileField(upload_to='uploads/')

    # Optional documents
    research_proposal = models.FileField(upload_to='uploads/', null=True, blank=True)
    additional_certificates = models.TextField(null=True, blank=True)  # JSON string
    other_files = models.TextField(null=True, blank=True)  # JSON string

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.major}"

    class Meta:
        db_table = 'application'
        ordering = ['-created_at']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'