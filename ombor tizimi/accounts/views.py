"""Views for authentication and account management."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, UserCreationForm, UserProfileForm


def is_admin(user):
    """Check if user is admin."""
    return user.is_staff or (hasattr(user, 'profile') and user.profile.role == 'admin')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def user_management(request):
    """User management view (admin only)."""
    users = User.objects.all().select_related('profile')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if action == 'delete' and user_id:
            if int(user_id) != request.user.id:
                user = User.objects.get(id=user_id)
                user.delete()
                messages.success(request, f'User {user.username} deleted successfully.')
            else:
                messages.error(request, 'You cannot delete your own account.')

        return redirect('user_management')

    context = {
        'users': users,
        'page_title': 'User Management',
    }
    return render(request, 'accounts/user_management.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def create_user(request):
    """Create new user view (admin only)."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('user_management')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'page_title': 'Create New User',
    }
    return render(request, 'accounts/create_user.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """User profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    context = {
        'form': form,
        'page_title': 'My Profile',
    }
    return render(request, 'accounts/profile.html', context)
