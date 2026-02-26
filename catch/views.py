from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Catch, Species, Venue, Method, Bait, LENGTH_CHOICES
from .forms import CatchForm, RegisterForm


class CatchListView(LoginRequiredMixin, ListView):
    model = Catch
    template_name = 'catch/catch_list.html'
    context_object_name = 'catches'
    paginate_by = 20

    def get_queryset(self):
        show_all = self.request.GET.get('all') == '1'
        if show_all:
            qs = Catch.objects.all()
        else:
            qs = Catch.objects.filter(user=self.request.user)
        species = self.request.GET.get('species')
        venue = self.request.GET.get('venue')
        method = self.request.GET.get('method')
        bait = self.request.GET.get('bait')
        length = self.request.GET.get('length')
        if species:
            qs = qs.filter(species_id=species)
        if venue:
            qs = qs.filter(venue_id=venue)
        if method:
            qs = qs.filter(method_id=method)
        if bait:
            qs = qs.filter(bait_id=bait)
        if length:
            qs = qs.filter(length=length)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['species_choices'] = Species.objects.all()
        ctx['venue_choices'] = Venue.objects.all()
        ctx['method_choices'] = Method.objects.all()
        ctx['bait_choices'] = Bait.objects.all()
        ctx['length_choices'] = LENGTH_CHOICES
        ctx['current_filters'] = {
            'species': self.request.GET.get('species', ''),
            'venue': self.request.GET.get('venue', ''),
            'method': self.request.GET.get('method', ''),
            'bait': self.request.GET.get('bait', ''),
            'length': self.request.GET.get('length', ''),
            'all': self.request.GET.get('all', ''),
        }
        ctx['show_all'] = self.request.GET.get('all') == '1'
        return ctx


class CatchCreateView(LoginRequiredMixin, CreateView):
    model = Catch
    form_class = CatchForm
    template_name = 'catch/catch_form.html'
    success_url = reverse_lazy('catch_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RegisterView(CreateView):
    """Simple registration page using the extended ``RegisterForm``.

    Upon successful registration the user is redirected to the login page
    so they can authenticate immediately.
    """
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
