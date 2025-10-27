from todoapp.models import Task
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# Create your views here.

@method_decorator(never_cache, name="dispatch")
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)

        searchInputText = self.request.GET.get("search","")
        if searchInputText:
            context["tasks"] = context["tasks"].filter(title__icontains=searchInputText)
        context["search"] = searchInputText

        return context


@method_decorator(never_cache, name="dispatch")
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@method_decorator(never_cache, name="dispatch")
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks")
    template_name = "task_form.html"
    context_object_name = "task"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(never_cache, name="dispatch")
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks")
    template_name = "task_form.html"
    context_object_name = "task"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    
@method_decorator(never_cache, name="dispatch")
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks")
    template_name = "task_delete.html"
    context_object_name = "task"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@method_decorator(never_cache, name="dispatch")
class TaskListLogin(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("tasks")


@method_decorator(never_cache, name="dispatch")
class RegisterTodoApp(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks")
    template_name = "register.html"

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


@method_decorator(never_cache, name="dispatch")
class AccountDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("login")
    template_name = "account_delete.html"

    def get_object(self):
        return self.request.user