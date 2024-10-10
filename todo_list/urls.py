from django.urls import path
from . import views
urlpatterns = [
    path('showtasks/',views.show_tasks ,name='showTasks'),
    path('searchtasks/',views.search ,name='searchTasks'),
    path('completetask/<int:task_id>/',views.complete_task,name='completeTask'),
    path('edittask/<int:task_id>/',views.edit_task,name='editTask'),
    path('deletetask/<int:task_id>/',views.delete_task,name='deleteTask'),
    path('filtertasks/<str:category>/',views.filter_tasks,name='filterTasks')
]
