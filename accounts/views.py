from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User
import re


def validate_password_strength(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'accounts/signup.html')
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messages.error(request, 'Invalid email format')
            return render(request, 'accounts/signup.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup.html')
        
        is_valid, password_msg = validate_password_strength(password)
        if not is_valid:
            messages.error(request, password_msg)
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/signup.html')
        
        try:
            user = User.objects.create_user(email=email, password=password)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error creating account')
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.email}!')
            
            if user.is_admin:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('landing')


@login_required
def user_dashboard(request):
    """User dashboard view"""
    return render(request, 'accounts/user_dashboard.html', {
        'user': request.user
    })


@login_required
def admin_dashboard(request):
    """Admin dashboard view - only accessible to admins"""
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page')
        return redirect('user_dashboard')

    return render(request, 'accounts/admin_dashboard.html', {
        'user': request.user
    })