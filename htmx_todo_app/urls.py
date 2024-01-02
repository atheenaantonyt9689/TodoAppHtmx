from django.urls import path

from htmx_todo_app.views import IndexView, TodoManagementView, add_to_items, \
    delete_to_item, update_status, update_to_do_item_title_and_due_date, SearchSampleIndexView, update_due_date

urlpatterns = [
    path('xx', IndexView.as_view(), name='htmx_todo_app_index'),
    path('', TodoManagementView.as_view(), name='htmx_todo_app_management'),
    path('todo/update/new/<int:id>', update_to_do_item_title_and_due_date, name='htmx_todo_app_update_new'),
    path('todo/delete/<int:pk>', delete_to_item, name='htmx_todo_app_delete'),
    path('todo/add/', add_to_items, name='htmx_todo_app_add_item'),
    path('todo/update/status/<int:pk>', update_status, name='htmx_todo_app_update_status'),
    path('todo/update/due_date/<int:pk>', update_due_date, name='htmx_todo_app_update_due_date'),
    path('search/sample', SearchSampleIndexView.as_view(), name='htmx_todo_app_search_sample'),


]
