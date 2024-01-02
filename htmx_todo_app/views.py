import datetime
from django.utils import timezone
from django.db.models import Q



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
            return render(request, 'htmx_todo_app/todo_functionality/partials/to_do_management.html', context)
        return super().get(request, *args, **kwargs)


class TodoManagementView(ListView):
    template_name = 'htmx_todo_app/todo_functionality/to_do_management.html'
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
            print("to_do_status ", to_do_status)
            sorting_with_date = self.request.GET.get('sorting_with_date', None)
            ascending = self.request.GET.get('ascending', None)
            print("ascendingffffffffffffffffffffffffffffffff ", ascending)
            print("sorting_with_date ", sorting_with_date)
            today_dateobj = datetime.date.today()

            if to_do_status == '0' and to_do_status is not None:
                to_dos = to_dos  #
                if sorting_with_date == 'created-date-asc':
                    to_dos = to_dos.filter(created__lte=timezone.now()).order_by('created')
                if sorting_with_date == 'due-date-desc':
                    to_dos = to_dos.filter(due_date__gte=today_dateobj).order_by('due_date')
            elif(to_do_status is not None and to_do_status != '0'):
                if to_do_status == 'has-due-date':
                    to_dos = to_dos.filter(due_date__gte=today_dateobj)
                    if sorting_with_date == 'due-date-desc':
                        to_dos = to_dos.filter(Q(due_date__lte=today_dateobj) | Q(due_date__gte=today_dateobj)).order_by('due_date')
                    if sorting_with_date == 'created-date-asc':
                        to_dos = to_dos.filter(created__lte=timezone.now()).order_by('created')
                else:
                    to_dos = to_dos.filter(status=to_do_status)
                    if sorting_with_date == 'created-date-asc':
                        to_dos = to_dos.filter(created__lte=timezone.now()).order_by('created')
                    if sorting_with_date == 'due-date-desc':
                        to_dos = to_dos.filter(Q(due_date__lte=today_dateobj) | Q(due_date__gte=today_dateobj)).order_by('due_date')

            self.template_name = 'htmx_todo_app/todo_functionality/partials/to_do_management.html'
        return to_dos


def add_to_items(request):
    print("Request POST", request.POST)
    # ceck of POST request is not empty
    if request.POST:
        context = {}
        to_item = request.POST.get('title')
        due_date = request.POST.get('due_date')
        print("hidden_due_date ", due_date)
        if len(to_item) > 0:
            to_do_obj = TodoItem.objects.create(title=to_item)
            if due_date:
                to_do_obj.due_date = due_date
            to_do_obj.save()
        context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/todo_functionality/partials/to_do_management.html', context=context)


def delete_to_item(request, pk):
    print("delete_ worked")
    context = {}
    if pk:
        TodoItem.objects.filter(id=pk).delete()
    context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/todo_functionality/partials/to_do_management.html', context=context)


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
    return render(request, 'htmx_todo_app/todo_functionality/partials/to_do_management.html', context=context)


def update_to_do_item_title_and_due_date(request, id):
    print("update_status")
    context = {}
    if id:
        todo_obj = TodoItem.objects.filter(id=id).first()
        title = request.GET.get('todo_name')
        if len(title) > 0:
            todo_obj.title = title
        todo_obj.save()
    print("Title saved successfully")
    context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/todo_functionality/partials/to_do_management.html', context=context)


def update_due_date(request,pk):
    print("update_due_date")
    context = {}
    id = pk
    if id:
        todo_obj = TodoItem.objects.filter(id=int(id)).first()
        due_date = request.GET.get('due_date')
        print("due_date ", due_date)
        if len(due_date) > 0:
            todo_obj.due_date = due_date
        todo_obj.save()
    print("Title savedd successfully")
    context['object_list'] = TodoItem.objects.all()
    return render(request, 'htmx_todo_app/todo_functionality/partials/to_do_management.html', context=context)


class SearchSampleIndexView(ListView):
    template_name = 'htmx_todo_app/search/search_sample.html'
    model = TodoItem
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        to_do_list = TodoItem.objects.all().order_by('created')
        if self.request.htmx:
            print("htmx request received")
            search_text = self.request.GET.get('search_text')
            print("search_text ", to_do_list)
            if len(search_text) > 0:
                to_do_list = to_do_list.filter(title__icontains=search_text).order_by('created')
            self.template_name = 'htmx_todo_app/search/partials/search_sample.html'
        return to_do_list




