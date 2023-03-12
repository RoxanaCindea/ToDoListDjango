from django.contrib.auth.views import LogoutView
from django.urls import path
from base import views


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),

    path('', views.TaskListView.as_view(), name='list-of-tasks'),
    path('details_task/<int:pk>/', views.TaskDetailView.as_view(), name='details-task'),
    path('create_task/', views.TaskCreateView.as_view(), name='create-task'),
    path('update_task/<int:pk>/', views.TaskUpdateView.as_view(), name='update-task'),
    path('delete-task<int:pk>/', views.TaskDeleteView.as_view(), name='delete-task'),
]
