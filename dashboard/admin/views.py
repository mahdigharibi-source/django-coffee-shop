

from django.views.generic import TemplateView

from address.models import Address


class DashboardAdminView(TemplateView):
    template_name = 'dashboard/admin/home.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardAdminView, self).get_context_data(**kwargs)
        context['address'] = Address.objects.all()
        return context