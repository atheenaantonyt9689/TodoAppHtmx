from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from django_htmx.http import HttpResponseClientRefresh

from htmx_todo_app.forms import TodoItemForm
from htmx_todo_app.models import TodoItem
from django.core.paginator import Paginator


# Create your views here.

class IndexView(TemplateView):
    template_name = 'htmx_todo_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # todo_items = TodoItem.objects.all()
        # print(todo_items)
        # context['to_do_list'] = todo_items
        return context

    def get(self, request, *args, **kwargs):
        print("get request")
        # htmx request
        if self.request.htmx:
            print("htmx request")
            to_do_list = TodoItem.objects.all()
            context = {'to_do_list': to_do_list}
            return render(request, 'htmx_todo_app/partials/to_do_management.html', context)
        return super().get(request, *args, **kwargs)


class TodoManagementView(ListView):
    template_name = 'htmx_todo_app/to_do_management.html'
    model = TodoItem
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context

    def get_queryset(self):
        to_dos = TodoItem.objects.all().order_by('created')
        if self.request.htmx:
            print("htmx request received")
            print(to_dos)
            to_do_status = self.request.GET.get('to_status_filter', None)
            sorting_with_date = self.request.GET.get('sorting_with_date', None)
            print("to_status_filter ", to_do_status)
            if to_do_status == '0':
                to_dos = to_dos  #
            if to_do_status is not None and to_do_status != '0':
                to_dos = to_dos.filter(status=to_do_status)
            #     Sorting
            print("sorting_with_date ", sorting_with_date)
            if sorting_with_date is not None:
                if sorting_with_date == 'due-date-desc':
                    to_dos = to_dos.order_by('-due_date')
                if sorting_with_date == 'created-date-asc':
                    to_dos = to_dos.order_by('created')
            self.template_name = 'htmx_todo_app/partials/to_do_management.html'
        return to_dos


def add_to_items(request):
    print("Request POST", request.POST)
    # ceck of POST request is not empty
    if request.POST:
        context = {}
        to_item = request.POST.get('title')
        due_date = request.POST.get('due_date')
        print("due_date ", due_date)
        if len(to_item) > 0:
            to_do_obj = TodoItem.objects.create(title=to_item,due_date=due_date)
            to_do_obj.save()
        context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/partials/to_do_management.html', context=context)


def delete_to_item(request, pk):
    print("delete_ worked")
    context = {}
    if pk:
        TodoItem.objects.filter(id=pk).delete()
    context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/partials/to_do_management.html', context=context)


def update_status(request, pk):
    print("update_status")
    context = {}
    if pk:
        todo_obj = TodoItem.objects.filter(id=pk).first()
        if todo_obj.status == 'active':
            todo_obj.status = 'completed'
        else:
            todo_obj.status = 'active'

        todo_obj.save()
    context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/partials/to_do_management.html', context=context)

# TODO need to correct
class TodoUpdateView(UpdateView):
    template_name = 'htmx_todo_app/update_to_do.html'
    model = TodoItem
    form_class = TodoItemForm
    success_url = reverse_lazy('htmx_todo_app_management')

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return self.model.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.htmx:
            context = {}
            to_id = self.kwargs.get('id')
            print("Get worked within the hTmsx request")
            context['form'] = TodoItemForm(instance=TodoItem.objects.get(id=to_id))
            context['to_id'] = to_id

            return render(request, 'htmx_todo_app/partials/to_do_update_modal.html', context=context)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.htmx:
            print("Post worked within the hTmsx request")
            to_id = self.kwargs.get('id')
            form = TodoItemForm(request.POST, instance=TodoItemForm.objects.get(id=to_id))
            form.save()

        return super().post(request, *args, **kwargs)
