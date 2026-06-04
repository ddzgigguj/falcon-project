from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings
from .models import Application
from FalconMain.telegram_utils import send_new_application_notification, send_application_status_update
import os
import zipfile
import io
from datetime import datetime


def allowed_file(filename):
"""Check if file extension is allowed"""
if '.' not in filename:
    return False
ext = filename.rsplit('.', 1)[1].lower()
return ext in settings.ALLOWED_EXTENSIONS


@login_required
@require_http_methods(["GET", "POST"])
def submit_application(request):
"""Submit scholarship application"""
if request.method == 'POST':
    full_name = request.POST.get('full_name', '').strip()
    passport_number = request.POST.get('passport_number', '').strip()
    major = request.POST.get('major', '').strip()
    study_type = request.POST.get('study_type', '').strip()
    
    if not all([full_name, passport_number, major, study_type]):
        messages.error(request, 'All fields are required')
        return render(request, 'applications/submit.html')
    
    required_files = [
        'cover_letter', 'cv', 'passport_file', 'personal_image',
        'highest_degree', 'transcript', 'recommendation_letter1',
        'recommendation_letter2', 'english_proficiency', 'medical_exam',
        'conduct_certificate', 'intro_video'
    ]
    
    files_dict = {}
    for field_name in required_files:
        file = request.FILES.get(field_name)
        if not file:
            messages.error(request, f'Missing required file: {field_name}')
            return render(request, 'applications/submit.html')
        
        if not allowed_file(file.name):
            messages.error(request, f'Invalid file type for: {field_name}')
            return render(request, 'applications/submit.html')
        
        files_dict[field_name] = file
    
    research_proposal = request.FILES.get('research_proposal')
    
    try:
        application = Application(
            user=request.user,
            full_name=full_name,
            passport_number=passport_number,
            major=major,
            study_type=study_type,
            **files_dict
        )
        
        if research_proposal and allowed_file(research_proposal.name):
            application.research_proposal = research_proposal
        
        application.save()
        
        try:
            send_new_application_notification(application)
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('user_applications')
    except Exception as e:
        messages.error(request, 'Error submitting application')
        return render(request, 'applications/submit.html')

return render(request, 'applications/submit.html')


@login_required
def user_applications(request):
"""View user's applications"""
applications = Application.objects.filter(user=request.user)
return render(request, 'applications/user_list.html', {
    'applications': applications
})


@login_required
def application_detail(request, app_id):
"""View application details"""
application = get_object_or_404(Application, id=app_id, user=request.user)
return render(request, 'applications/detail.html', {
    'application': application
})


@login_required
def admin_applications(request):
"""Admin view of all applications"""
if not request.user.is_admin:
    messages.error(request, 'You do not have permission to access this page')
    return redirect('user_dashboard')

applications = Application.objects.all().select_related('user')
return render(request, 'applications/admin_list.html', {
    'applications': applications
})


@login_required
def admin_application_detail(request, app_id):
"""Admin view of application details"""
if not request.user.is_admin:
    messages.error(request, 'You do not have permission to access this page')
    return redirect('user_dashboard')

application = get_object_or_404(Application, id=app_id)

if request.method == 'POST':
    status = request.POST.get('status')
    if status in dict(Application.STATUS_CHOICES):
        old_status = application.status
        application.status = status
        application.save()
        
        try:
            send_application_status_update(application, old_status, status)
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
        
        messages.success(request, 'Application status updated')
        return redirect('admin_application_detail', app_id=app_id)

return render(request, 'applications/admin_detail.html', {
    'application': application
})


@login_required
def download_application_files(request, app_id):
"""Download all application files as ZIP"""
if not request.user.is_admin:
    messages.error(request, 'You do not have permission to access this page')
    return redirect('user_dashboard')

application = get_object_or_404(Application, id=app_id)

zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    files_to_zip = [
        (application.cover_letter, 'Cover_Letter'),
        (application.cv, 'CV'),
        (application.passport_file, 'Passport'),
        (application.personal_image, 'Personal_Image'),
        (application.highest_degree, 'Highest_Degree'),
        (application.transcript, 'Transcript'),
        (application.recommendation_letter1, 'Recommendation_Letter_1'),
        (application.recommendation_letter2, 'Recommendation_Letter_2'),
        (application.english_proficiency, 'English_Proficiency'),
        (application.medical_exam, 'Medical_Exam'),
        (application.conduct_certificate, 'Conduct_Certificate'),
        (application.intro_video, 'Intro_Video'),
    ]
    
    if application.research_proposal:
        files_to_zip.append((application.research_proposal, 'Research_Proposal'))
    
    for file_field, display_name in files_to_zip:
        if file_field:
            try:
                file_path = file_field.path
                if os.path.exists(file_path):
                    ext = os.path.splitext(file_path)[1]
                    zip_file.write(file_path, f"{display_name}{ext}")
            except Exception:
                pass
    
    readme_content = f"""Application Details
===================

Full Name: {application.full_name}
Email: {application.user.email}
Passport Number: {application.passport_number}
Major: {application.major}
Study Type: {application.study_type}
Status: {application.status}
Submitted: {application.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Downloaded on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    zip_file.writestr('README.txt', readme_content)

zip_buffer.seek(0)

safe_name = "".join(c for c in application.full_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
zip_filename = f"application_{safe_name}_{application.id}.zip"

response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
return response