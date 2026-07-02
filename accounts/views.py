from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, StudentRegistrationForm, CustomLoginForm, UserUpdateForm, StudentUpdateForm
from .models import Student

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:home')

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            # If user is a student, redirect to student profile creation
            if user.user_type == 'student':
                login(request, user)
                messages.success(request, 'Account created successfully! Please complete your student profile.')
                return redirect('accounts:student_profile')
            else:
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('dashboard:home')
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form
    })

@login_required
def student_profile(request):
    # Check if student profile already exists
    try:
        student = request.user.student
        return redirect('dashboard:home')
    except Student.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, 'Student profile created successfully!')
            return redirect('dashboard:home')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/student_profile.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if request.user.is_student():
            try:
                student_form = StudentUpdateForm(request.POST, instance=request.user.student)
            except Student.DoesNotExist:
                return redirect('accounts:student_profile')
        else:
            student_form = None
        
        if user_form.is_valid() and (student_form is None or student_form.is_valid()):
            user_form.save()
            if student_form:
                student_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        
        if request.user.is_student():
            try:
                student_form = StudentUpdateForm(instance=request.user.student)
            except Student.DoesNotExist:
                return redirect('accounts:student_profile')
        else:
            student_form = None
    
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'student_form': student_form
    })
