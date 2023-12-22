from django import forms

from htmx_todo_app.models import TodoItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
