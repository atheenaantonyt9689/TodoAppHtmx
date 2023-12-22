from django.urls import path

from htmx_todo_app.views import IndexView, TodoManagementView, TodoUpdateView, add_to_items, \
    delete_to_item, update_status

urlpatterns = [
    path('xx',IndexView.as_view(),name='htmx_todo_app_index'),
    path('',TodoManagementView.as_view(),name='htmx_todo_app_management'),
    path('todo/update/<int:id>',TodoUpdateView.as_view(),name='htmx_todo_app_update'),
    path('todo/delete/<int:pk>',delete_to_item,name='htmx_todo_app_delete'),
    path('todo/add/', add_to_items,name='htmx_todo_app_add_item'),
    path('todo/update/status/<int:pk>', update_status,name='htmx_todo_app_update_status'),


]
