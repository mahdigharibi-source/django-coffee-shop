from django.contrib.auth import login
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, DetailView

from accounts.forms import CustomUserCreationForm, CustomUserLoginForm
from accounts.models import Profile, CustomUser


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'registration/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'registration/profile.html'
    fields = ['full_name', 'phone_number']

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile')


class RegisterView(CreateView):
    model = CustomUser
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('website:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
