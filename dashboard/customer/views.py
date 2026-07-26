from django.views.generic import TemplateView

from address.models import Address


class DashboardCustomerView(TemplateView):
    template_name = 'dashboard/customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardCustomerView, self).get_context_data(**kwargs)
        context['address'] = Address.objects.all()
        return context