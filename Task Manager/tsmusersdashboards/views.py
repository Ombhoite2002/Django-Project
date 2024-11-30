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




def admin_panel(request):
    
    total_employees = Employee.objects.count()
    
    
    total_tasks = Task.objects.count()
    
   
    completed_tasks = Task.objects.filter(status="Completed").count()
    
    
    failed_tasks = Task.objects.filter(status="Failed").count()
    
    
    pending_tasks = Task.objects.filter(status="In Progress").count()
    
    
    overdue_tasks = Task.objects.filter(due_date__lt=timezone.now()).exclude(status="Completed").count()

   
    urgent_tasks = Task.objects.filter(priority__iexact="Urgent").count()
    
    
    high_tasks = Task.objects.filter(priority__iexact="High").count()

   
    medium_tasks = Task.objects.filter(priority__iexact="Medium").count()

   
    low_tasks = Task.objects.filter(priority__iexact="Low").count()

    
    tasks = Task.objects.all()

    
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
        "tasks": tasks,  
    }

    
    return render(request, 'tsmusersdashboards/admin_dashboard.html', context)

def employee_dashboard(request, employee_id):
   
    employee = get_object_or_404(Employee, id=employee_id)

   
    employee_profile, created = EmployeeProfile.objects.get_or_create(employee=employee)

    if created:
        
        employee_profile.role = "Default Role"
        employee_profile.save()

    
    tasks = Task.objects.filter(assigned_employees=employee_profile)

   
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="Completed").count()
    pending_tasks = tasks.filter(status="In Progress").count()
    failed_tasks = tasks.filter(status="Failed").count()

    
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
   
    logout(request)
    
    
    from django.contrib import messages
    messages.success(request, "You have been logged out successfully.")
    
   
    return redirect('login')

