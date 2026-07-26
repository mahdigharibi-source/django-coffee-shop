from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from accounts.models import UserType


class DashboardHomeView(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == UserType.ADMIN:
                return redirect(reverse_lazy('dashboard:admin:home'))
            else:
                return redirect(reverse_lazy('dashboard:customer:home'))
        else:
            return JsonResponse({'message': 'You are not logged in'})