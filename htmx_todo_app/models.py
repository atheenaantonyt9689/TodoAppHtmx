from django.db import models


# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=(('active', 'active'), ('completed', 'completed')), default='active')
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
