from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import logout
from tsmusers.models import Employee,EmployeeProfile
from tsmtasks.models import Task
from django.utils import timezone
from django.http import HttpResponseNotFound
import json
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


# Create your views here.

def admin_panel(request):
    # Fetch total number of employees
    total_employees = Employee.objects.count()
    
    # Fetch total number of tasks
    total_tasks = Task.objects.count()
    
    # Fetch total number of completed tasks
    completed_tasks = Task.objects.filter(status="Completed").count()
    
    # Fetch total number of failed tasks
    failed_tasks = Task.objects.filter(status="Failed").count()
    
    # Fetch total number of pending tasks
    pending_tasks = Task.objects.filter(status="In Progress").count()
    
    # Fetch overdue tasks
    overdue_tasks = Task.objects.filter(due_date__lt=timezone.now()).exclude(status="Completed").count()

    # Fetch tasks with urgent priority
    urgent_tasks = Task.objects.filter(priority__iexact="Urgent").count()
    
    # Fetch tasks with high priority
    high_tasks = Task.objects.filter(priority__iexact="High").count()

    # Fetch tasks with medium priority
    medium_tasks = Task.objects.filter(priority__iexact="Medium").count()

    # Fetch tasks with low priority
    low_tasks = Task.objects.filter(priority__iexact="Low").count()

    # Fetch all tasks for task management section (optional: limit to recent tasks if needed)
    tasks = Task.objects.all()

    # Context to pass to the template
    context = {
        "total_employees": total_employees,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "pending_tasks": pending_tasks,
        "overdue_tasks": overdue_tasks,
        "urgent_tasks": urgent_tasks,
        "high_tasks": high_tasks,
        "medium_tasks": medium_tasks,
        "low_tasks": low_tasks,
        "tasks": tasks,  # For task management section
    }

    # Render the admin dashboard with the context
    return render(request, 'tsmusersdashboards/admin_dashboard.html', context)

def employee_dashboard(request, employee_id):
    # Fetch the Employee object
    employee = get_object_or_404(Employee, id=employee_id)

    # Get or create the EmployeeProfile
    employee_profile, created = EmployeeProfile.objects.get_or_create(employee=employee)

    if created:
        # Initialize default values for the new profile if necessary
        employee_profile.role = "Default Role"
        employee_profile.save()

    # Fetch tasks assigned to the employee's profile
    tasks = Task.objects.filter(assigned_employees=employee_profile)

    # Calculate task stats
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="Completed").count()
    pending_tasks = tasks.filter(status="In Progress").count()
    failed_tasks = tasks.filter(status="Failed").count()

    # Context for the template
    context = {
        "tasks": tasks,
        "employee_name": f"{employee_profile.first_name} {employee_profile.last_name}",
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "failed_tasks": failed_tasks,
        "current_year": 2024,
    }

    return render(request, "tsmusersdashboards/employee_dashboard.html", context)


def update_task_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            new_status = data.get('status')

            # Update the task status in the database
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()

            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


def employee_logout(request):
    # Perform the logout operation
    logout(request)
    
    # Optionally, add a logout message (if using Django's messages framework)
    from django.contrib import messages
    messages.success(request, "You have been logged out successfully.")
    
    # Redirect to the login page or home page
    return redirect('login')

