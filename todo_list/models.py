from django.db import models
from accounts.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    CATEGORY_CHOICES = [
        ('Personal','Personal'),
        ('Work', 'Work'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES, default='Medium')
    category = models.CharField(max_length=10,choices=CATEGORY_CHOICES, default='Personal')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_by')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT,related_name='assigned_to',blank=True,null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    due_time = models.TimeField(blank=True, null=True) 

    def __str__(self):
        return self.title



