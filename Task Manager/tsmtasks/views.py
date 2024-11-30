from django.shortcuts import render,redirect,get_object_or_404
from tsmusers.models import EmployeeProfile,Employee
from .models import Task
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import Case, When, Value
from datetime import datetime
from django.db.models import IntegerField

# Create your views here.

def task_list(request):
    return render(request,'tsmtasks/task_list.html')

def task_detail(request):
    # Retrieve sorting and filtering parameters
    sort_by = request.GET.get('sort_by', '')
    priority_filter = request.GET.get('priority', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')

    # Retrieve all tasks
    tasks = Task.objects.select_related('assigned_employees')

    # Apply sorting
    if sort_by == 'role':
        tasks = tasks.order_by('assigned_employees__role')
    elif sort_by == 'priority':
        tasks = tasks.annotate(
            priority_order=Case(
                When(priority='Urgent', then=Value(1)),
                When(priority='High', then=Value(2)),
                When(priority='Medium', then=Value(3)),
                When(priority='Low', then=Value(4)),
                default=Value(5),
                output_field=IntegerField()
            )
        ).order_by('priority_order')
    elif sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'status':
        tasks = tasks.order_by('status')

    # Apply filters to tasks
    if priority_filter:
        tasks = tasks.filter(priority__iexact=priority_filter)  # Case-insensitive match
    if role_filter:
        tasks = tasks.filter(assigned_employees__role=role_filter)
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Retrieve all employees (for total count)
    employees = EmployeeProfile.objects.all()

    # Apply role filter to employees (if set)
    if role_filter:
        employees = employees.filter(role=role_filter)

    # Count all employees (including those without tasks)
    total_employees = employees.count()

    # Get distinct roles for dropdown
    distinct_roles = EmployeeProfile.objects.values_list('role', flat=True).distinct()

    # Prepare context
    context = {
        'tasks': tasks,
        'distinct_roles': distinct_roles,
        'employees': employees,
        'total_employees': total_employees,
    }
    return render(request, 'tsmtasks/task_detail.html', context)




def task_form(request):
    # Fetch all employee profiles
    employees = EmployeeProfile.objects.all()

    # Handle form submission if POST request
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        assign_to_id = request.POST.get('assign_to')  # This will hold the selected employee's ID
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        # Fetch the EmployeeProfile instance based on the provided ID
        assigned_employee = EmployeeProfile.objects.get(id=assign_to_id)

        # Create the task instance
        Task.objects.create(
            task_name=task_name,
            task_description=task_description,
            assigned_employees=assigned_employee,  # Correct field name
            priority=priority,
            due_date=due_date,
        )

        return redirect('taskdetails')  # Replace with your success URL or redirect

    return render(request, 'tsmtasks/task_form.html', {'employees': employees})

def task_update(request, pk):
    # Fetch the task object to update
    task = get_object_or_404(Task, pk=pk)
    # Fetch all employee profiles
    employee_profiles = EmployeeProfile.objects.all()

    if request.method == 'POST':
        # Get data from the form
        task_name = request.POST.get('task_name', task.task_name)
        task_description = request.POST.get('task_description', task.task_description)
        assign_to_id = request.POST.get('assign_to')
        priority = request.POST.get('priority', task.priority)
        due_date = request.POST.get('due_date', task.due_date)

        # Check if assign_to is not empty, otherwise keep the existing value
        if assign_to_id:
            assigned_employee_profile = get_object_or_404(EmployeeProfile, pk=assign_to_id)
        else:
            assigned_employee_profile = task.assigned_employee_profile  # Keep existing employee profile if not changed

        # Validation and Update Task Object
        task.task_name = task_name
        task.task_description = task_description
        task.assigned_employee_profile = assigned_employee_profile
        task.priority = priority
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()  # Convert string to date object

        # Save the updated task
        task.save()

        # Optionally, you can redirect after saving to avoid resubmission on refresh
        return redirect('task_update', pk=task.pk)

    # Render form with existing task details
    context = {
        'task': task,
        'employee_profiles': employee_profiles,
    }
    return render(request, 'tsmtasks/task_update.html', context)

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('taskdetails')  # Redirect to the task details page after deletion