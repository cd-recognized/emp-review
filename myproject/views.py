from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import EmployeeResponse, ManagerResponse, HRComment

# --------------------------
# Webhook-related Views
# --------------------------

@csrf_exempt
def formstack_webhook(request):
    if request.method == 'POST':
        data = request.POST

        # Process incoming webhook data
        EmployeeResponse.objects.create(
            employee_name=data.get('employee_name', ''),
            employee_email=data.get('employee_email', ''),
            manager_email=data.get('manager_email', ''),
            achievements=data.get('achievements', ''),
            improvements=data.get('improvements', ''),
            goal_1=data.get('goal_1', ''),
            goal_2=data.get('goal_2', ''),
            goal_3=data.get('goal_3', ''),
            progress=data.get('progress', ''),
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# --------------------------
# Manager and HR Views
# --------------------------

@login_required
def manager_dashboard(request):
    responses = EmployeeResponse.objects.filter(manager_email=request.user.email)
    return render(request, 'manager_dashboard.html', {'responses': responses})

@login_required
def hr_dashboard(request):
    responses = EmployeeResponse.objects.all()
    return render(request, 'hr_dashboard.html', {'responses': responses})

@login_required
def add_manager_response(request, response_id):
    response = get_object_or_404(EmployeeResponse, id=response_id)
    if request.method == 'POST':
        ManagerResponse.objects.create(
            employee_response=response,
            manager_email=request.user.email,
            response_text=request.POST.get('response_text')
        )
        return redirect('manager_dashboard')
    return render(request, 'add_manager_response.html', {'response': response})

@login_required
def add_hr_comment(request, response_id):
    response = get_object_or_404(EmployeeResponse, id=response_id)
    if request.method == 'POST':
        HRComment.objects.create(
            employee_response=response,
            hr_email=request.user.email,
            comment_text=request.POST.get('comment_text')
        )
        return redirect('hr_dashboard')
    return render(request, 'add_hr_comment.html', {'response': response})