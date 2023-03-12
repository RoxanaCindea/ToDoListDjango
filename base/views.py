from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, FormView
from base.models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list-of-tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list-of-tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list-of-tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    template_name = 'base/list_of_tasks.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/details_task.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'base/create_task.html'
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('list-of-tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'base/update_task.html'
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('list-of-tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'base/delete_task.html'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('list-of-tasks')
