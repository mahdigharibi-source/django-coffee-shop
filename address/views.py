from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DeleteView

from address.forms import AddressForm
from address.models import Address


class AddressListView(ListView):
    template_name = 'address/address-list.html'
    model = Address
    context_object_name = 'addresses'


class AddressEditView(UpdateView):
    template_name = 'address/address.html'
    model = Address
    form_class = AddressForm
    success_url = '/'


    def get_object(self, queryset=None):
        return Address.objects.get(
            pk=self.kwargs.get('pk'),
            user=self.request.user
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressCreateView(CreateView):
    template_name = 'address/address.html'
    model = Address
    form_class = AddressForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user

        address = Address.objects.filter(user=self.request.user).exists()

        if not address:
            form.instance.is_default = True

        elif form.cleaned_data['is_default']:
            Address.objects.filter(user=self.request.user).update(is_default=False)

        return super().form_valid(form)


class SetAddressDefault(View):
    def post(self, request, *args, **kwargs):
        default_address_id = request.POST.get('address_id')
        if default_address_id:
            Address.objects.filter(user=request.user).update(is_default=False)

            address = Address.objects.get(id=default_address_id)
            address.is_default = True
            address.save()

            return redirect('address:address-list')
        return redirect('/')

class AddressDeleteView(View):
    def post(self, request, *args, **kwargs):
        address_id = request.POST.get('address_id')
        Address.objects.filter(id=address_id).delete()
        return HttpResponseRedirect('/')
