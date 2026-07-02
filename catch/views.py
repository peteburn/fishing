from collections import defaultdict

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.forms import modelformset_factory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from .models import Catch, Species, Venue, Method, Bait
from .forms import CatchForm, RegisterForm

class CatchDetailView(LoginRequiredMixin, DetailView):
    model = Catch
    template_name = 'catch/catch_detail.html'
    context_object_name = 'catch'

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
            try:
                qs = qs.filter(length=float(length))
            except (ValueError, TypeError):
                pass
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['species_choices'] = Species.objects.all()
        ctx['venue_choices'] = Venue.objects.all()
        ctx['method_choices'] = Method.objects.all()
        ctx['bait_choices'] = Bait.objects.all()
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


class LeaderboardView(LoginRequiredMixin, TemplateView):
    template_name = 'catch/leaderboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        catches = Catch.objects.select_related('user', 'species').order_by('species_id', '-length', 'date', 'pk')

        user_stats = {}
        species_users = defaultdict(set)
        species_catches = defaultdict(list)
        special_bonus_species = {'gudgeon', 'minnow', 'stickleback'}

        for catch in catches:
            stats = user_stats.setdefault(
                catch.user_id,
                {
                    'user': catch.user,
                    'species_ids': set(),
                    'special_bonus_awarded': False,
                },
            )
            stats['species_ids'].add(catch.species_id)
            species_users[catch.species_id].add(catch.user_id)
            species_catches[catch.species_id].append(catch)
            if catch.species.name.strip().lower() in special_bonus_species:
                stats['special_bonus_awarded'] = True

        leaderboard = []
        for stats in user_stats.values():
            species_points = len(stats['species_ids'])
            bonus_points = 1 if stats['special_bonus_awarded'] else 0
            leaderboard.append({
                'user': stats['user'],
                'species_points': species_points,
                'bonus_points': bonus_points,
                'total_points': species_points + bonus_points,
            })

        for species_id, catches_for_species in species_catches.items():
            if len(species_users[species_id]) < 2:
                continue
            scored_catches = [catch for catch in catches_for_species if catch.length is not None]
            if not scored_catches:
                continue
            max_length = max(catch.length for catch in scored_catches)
            winners = [catch for catch in scored_catches if catch.length == max_length]
            if len(winners) != 1:
                continue
            winner = winners[0]
            for row in leaderboard:
                if row['user'].id == winner.user_id:
                    row['bonus_points'] += 1
                    row['total_points'] += 1
                    break

        leaderboard.sort(
            key=lambda row: (
                -row['total_points'],
                -row['species_points'],
                row['user'].username.lower(),
            )
        )
        ctx['leaderboard'] = leaderboard
        return ctx


class CatchCreateView(LoginRequiredMixin, CreateView):
    model = Catch
    form_class = CatchForm
    template_name = 'catch/catch_form.html'
    success_url = reverse_lazy('catch_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Save with picture if present
        if self.request.FILES:
            form.instance.picture = self.request.FILES.get('picture')
        return super().form_valid(form)


class CatchUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Catch
    form_class = CatchForm
    template_name = 'catch/catch_form.html'
    success_url = reverse_lazy('catch_list')

    def test_func(self):
        return self.get_object().user == self.request.user

class CatchDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Catch
    template_name = 'catch/catch_confirm_delete.html'
    success_url = reverse_lazy('catch_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['redirect_url'] = self.success_url
        return ctx


class RegisterView(CreateView):
    """Simple registration page using the extended ``RegisterForm``.

    Upon successful registration the user is redirected to the login page
    so they can authenticate immediately.
    """
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


@user_passes_test(lambda u: u.is_superuser)
def lookup_admin(request):
    """Superuser-only page to maintain the various lookup models.

    Four formsets (species, venue, method, bait) are displayed on a single
    page.  Each formset allows adding, editing and deleting rows.  The
    ``user_passes_test`` decorator ensures only superusers can access it.
    """
    SpeciesFormSet = modelformset_factory(Species, fields=('name',), can_delete=True, extra=1)
    VenueFormSet = modelformset_factory(Venue, fields=('name',), can_delete=True, extra=1)
    MethodFormSet = modelformset_factory(Method, fields=('name',), can_delete=True, extra=1)
    BaitFormSet = modelformset_factory(Bait, fields=('name',), can_delete=True, extra=1)

    if request.method == 'POST':
        species_fs = SpeciesFormSet(request.POST, prefix='species')
        venue_fs = VenueFormSet(request.POST, prefix='venue')
        method_fs = MethodFormSet(request.POST, prefix='method')
        bait_fs = BaitFormSet(request.POST, prefix='bait')
        if species_fs.is_valid() and venue_fs.is_valid() and method_fs.is_valid() and bait_fs.is_valid():
            all_saved = True
            try:
                species_fs.save()
            except ProtectedError as e:
                all_saved = False
                for form in species_fs.forms:
                    form.add_error(None, f"Cannot delete Species: {str(e)}. It is referenced by existing catches.")
            try:
                venue_fs.save()
            except ProtectedError as e:
                all_saved = False
                for form in venue_fs.forms:
                    form.add_error(None, f"Cannot delete Venue: {str(e)}. It is referenced by existing catches.")
            try:
                method_fs.save()
            except ProtectedError as e:
                all_saved = False
                for form in method_fs.forms:
                    form.add_error(None, f"Cannot delete Method: {str(e)}. It is referenced by existing catches.")
            try:
                bait_fs.save()
            except ProtectedError as e:
                all_saved = False
                for form in bait_fs.forms:
                    form.add_error(None, f"Cannot delete Bait: {str(e)}. It is referenced by existing catches.")
            if all_saved:
                return redirect('lookup_admin')
    else:
        species_fs = SpeciesFormSet(prefix='species')
        venue_fs = VenueFormSet(prefix='venue')
        method_fs = MethodFormSet(prefix='method')
        bait_fs = BaitFormSet(prefix='bait')

    return render(request, 'catch/lookup_admin.html', {
        'species_fs': species_fs,
        'venue_fs': venue_fs,
        'method_fs': method_fs,
        'bait_fs': bait_fs,
    })
