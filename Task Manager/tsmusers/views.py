from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee,EmployeeProfile
from tsmtasks.models import Task
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.decorators import login_required

class CustomAuthBackend(BaseBackend):
    """
    Custom authentication backend to authenticate against the Employee model.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Fetch the employee record with the given username
            employee = Employee.objects.get(username=username)

            if check_password(password, employee.password):
                return employee
        except Employee.DoesNotExist:
            return None  

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')

        try:
            validate_email(email)  
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return redirect('signup')

        
        if Employee.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if Employee.objects.filter(email=email.lower()).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        
        hashed_password = make_password(password)
        employee = Employee(username=username, email=email, password=hashed_password)
        employee.save()

        
        request.session['employee_id'] = employee.id
        request.session['username'] = employee.username

        messages.success(request, "Signup successful! Welcome!")
        return redirect('home')  

    return render(request, 'registration/signup.html')  # Render signup template

def login(request):
    if request.method == "POST":
        role = request.POST.get('role')
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        if not role or not username or not password:
            messages.error(request, "All fields are required.")
            return redirect('login')

        
        if role == "employee":
            try:
                employee = Employee.objects.get(username=username)
                if check_password(password, employee.password):
                    
                    request.session['employee_id'] = employee.id
                    request.session['employee_username'] = employee.username

                    messages.success(request, f"Welcome, {employee.username}!")
                    return redirect('employeedashboard', employee_id=employee.id)  
                else:
                    messages.error(request, "Invalid credentials for employee.")
            except Employee.DoesNotExist:
                messages.error(request, "Employee not found.")
            return redirect('login')

       
        elif role == "admin":
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                
                auth_login(request, user)
                request.session['admin_username'] = user.username
                messages.success(request, f"Welcome, Admin {user.username}!")
                return redirect('adminpanel')  
            else:
                messages.error(request, "Invalid credentials or you are not authorized as an admin.")
            return redirect('login')

        else:
            messages.error(request, "Invalid role selected.")
            return redirect('login')

    return render(request, 'registration/login.html')  

def employeeProfile(request):
    try:
        
        employee = Employee.objects.get(id=request.session.get('employee_id'))
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found.")
        return redirect('login')  

    
    profile, created = EmployeeProfile.objects.get_or_create(employee=employee)

    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if not first_name or not last_name or not age or not gender or not role or not address or not phone_number:
            messages.error(request, "All fields are required.")
            return render(request, 'tsmusers/employee_profile.html', {'profile': profile})

        try:
            age = int(age)
        except ValueError:
            messages.error(request, "Age must be a valid number.")
            return render(request, 'tsmusers/employee_profile.html', {'profile': profile})

        
        profile.first_name = first_name
        profile.middle_name = middle_name
        profile.last_name = last_name
        profile.age = age
        profile.gender = gender
        profile.role = role
        profile.address = address
        profile.phone_number = phone_number
        profile.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('employeeprofile')

    return render(request, 'tsmusers/employee_profile.html', {'profile': profile, 'created': created})


def employee_details(request):
    
    search_query = request.GET.get('search', '')

   
    employees = Employee.objects.select_related('profile')  

    if search_query:
        employees = employees.filter(
            Q(profile__first_name__icontains=search_query) |  
            Q(username__icontains=search_query) |            
            Q(email__icontains=search_query) |               
            Q(profile__role__icontains=search_query) |       
            Q(profile__phone_number__icontains=search_query) 
        )

    return render(request, 'tsmusers/employee_details.html', {'employees': employees})

def view_profile(request, employee_id):
    
    employee = get_object_or_404(Employee, id=employee_id)

   
    employee_profile = employee.profile

   
    tasks = Task.objects.filter(assigned_employees=employee_profile)

    return render(request, 'tsmusers/view_profile.html', {
        'employee': employee,
        'profile': employee_profile,
        'tasks': tasks
    })


