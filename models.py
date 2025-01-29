# models.py
from django.db import models

class EmployeeResponse(models.Model):
    employee_name = models.CharField(max_length=255)
    employee_email = models.EmailField()
    manager_email = models.EmailField()
    achievements = models.TextField()
    improvements = models.TextField()
    goal_1 = models.TextField()
    goal_2 = models.TextField()
    goal_3 = models.TextField()
    progress = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class ManagerResponse(models.Model):
    employee_response = models.ForeignKey(EmployeeResponse, on_delete=models.CASCADE, related_name='manager_responses')
    manager_email = models.EmailField()
    response_text = models.TextField()  # JSON or structured text for multiple responses
    submitted_at = models.DateTimeField(auto_now_add=True)

class HRComment(models.Model):
    employee_response = models.ForeignKey(EmployeeResponse, on_delete=models.CASCADE, related_name='hr_comments')
    hr_email = models.EmailField()
    comment_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)