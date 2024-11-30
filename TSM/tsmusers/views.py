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

            # Verify the hashed password
            if check_password(password, employee.password):
                return employee
        except Employee.DoesNotExist:
            return None  # Return None if the user is not found or the password is incorrect

    def get_user(self, user_id):
        try:
            return Employee.objects.get(pk=user_id)
        except Employee.DoesNotExist:
            return None

# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        # Input validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')

        try:
            validate_email(email)  # Validate email format
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return redirect('signup')

        # Check if username or email already exists
        if Employee.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        if Employee.objects.filter(email=email.lower()).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        # Hash the password before saving
        hashed_password = make_password(password)
        employee = Employee(username=username, email=email, password=hashed_password)
        employee.save()

        # Simulating login by setting session data (if using custom logic)
        request.session['employee_id'] = employee.id
        request.session['username'] = employee.username

        messages.success(request, "Signup successful! Welcome!")
        return redirect('home')  # Redirect to the homepage or another page after signup

    return render(request, 'registration/signup.html')  # Render signup template

def login(request):
    if request.method == "POST":
        role = request.POST.get('role')
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        if not role or not username or not password:
            messages.error(request, "All fields are required.")
            return redirect('login')

        # Handle Employee Login
        if role == "employee":
            try:
                employee = Employee.objects.get(username=username)
                if check_password(password, employee.password):
                    # Store employee info in the session
                    request.session['employee_id'] = employee.id
                    request.session['employee_username'] = employee.username

                    messages.success(request, f"Welcome, {employee.username}!")
                    return redirect('employeedashboard', employee_id=employee.id)  # Redirect to employee dashboard
                else:
                    messages.error(request, "Invalid credentials for employee.")
            except Employee.DoesNotExist:
                messages.error(request, "Employee not found.")
            return redirect('login')

        # Handle Admin Login (Superuser)
        elif role == "admin":
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                # Log in the superuser
                auth_login(request, user)
                request.session['admin_username'] = user.username
                messages.success(request, f"Welcome, Admin {user.username}!")
                return redirect('adminpanel')  # Redirect to admin panel
            else:
                messages.error(request, "Invalid credentials or you are not authorized as an admin.")
            return redirect('login')

        else:
            messages.error(request, "Invalid role selected.")
            return redirect('login')

    return render(request, 'registration/login.html')  # Render the login template

def employeeProfile(request):
    try:
        # Get the logged-in employee
        employee = Employee.objects.get(id=request.session.get('employee_id'))
    except Employee.DoesNotExist:
        messages.error(request, "Employee not found.")
        return redirect('login')  # Redirect to login if the employee is not found

    # Get or create the employee's profile
    profile, created = EmployeeProfile.objects.get_or_create(employee=employee)

    if request.method == 'POST':
        # Process the form data (same as before)
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

        # Update profile
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
    # Get the search query from GET request
    search_query = request.GET.get('search', '')

    # Filter employees based on the search query
    employees = Employee.objects.select_related('profile')  # Use `select_related` for efficient querying

    if search_query:
        employees = employees.filter(
            Q(profile__first_name__icontains=search_query) |  # Filter by first name
            Q(username__icontains=search_query) |            # Filter by username
            Q(email__icontains=search_query) |               # Filter by email
            Q(profile__role__icontains=search_query) |       # Filter by role
            Q(profile__phone_number__icontains=search_query) # Filter by phone number
        )

    return render(request, 'tsmusers/employee_details.html', {'employees': employees})

def view_profile(request, employee_id):
    # Get the specific employee by ID or return a 404 if not found
    employee = get_object_or_404(Employee, id=employee_id)

    # Access the profile through the employee's profile
    employee_profile = employee.profile

    # Fetch tasks related to the employee using the ForeignKey relationship
    tasks = Task.objects.filter(assigned_employees=employee_profile)

    return render(request, 'tsmusers/view_profile.html', {
        'employee': employee,
        'profile': employee_profile,
        'tasks': tasks
    })


