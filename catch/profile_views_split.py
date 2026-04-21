from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .profile_forms import ProfilePasswordChangeForm, ProfilePictureForm

class PasswordChangeOnlyView(LoginRequiredMixin, View):
    template_name = 'catch/password_form.html'
    success_url = reverse_lazy('profile_password_done')

    def get(self, request, *args, **kwargs):
        form = ProfilePasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form, 'user': request.user})

    def post(self, request, *args, **kwargs):
        form = ProfilePasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'user': request.user})

class PictureUpdateOnlyView(LoginRequiredMixin, View):
    template_name = 'catch/picture_form.html'
    success_url = reverse_lazy('profile_edit_done')

    def get(self, request, *args, **kwargs):
        picture_form = ProfilePictureForm(instance=request.user.profile)
        return render(request, self.template_name, {'picture_form': picture_form, 'user': request.user})

    def post(self, request, *args, **kwargs):
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if picture_form.is_valid():
            picture_form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'picture_form': picture_form, 'user': request.user})
