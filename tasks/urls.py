from django.urls import path

from . import views

urlpatterns = [
    path('helloWorld', views.helloWorld), # A função views.helloWorld foi importada de views
    path('', views.taskList, name='task-list'),
    path('task/<int:id>', views.taskView, name='task-view'),
    path('newtask/', views.newTask, name='new-task'),
    path('edit/<int:id>', views.editTasks, name='edit-task'),
    path('delete/<int:id>', views.deleteTasks, name='delete-task'),
    path('yourname/<str:name>', views.yourName, name='your-name'),
]