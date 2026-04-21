from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from .profile_forms import ProfilePasswordChangeForm, ProfilePictureForm


class ProfileEditView(LoginRequiredMixin, View):
    template_name = 'catch/profile_form.html'
    success_url = reverse_lazy('profile_edit_done')

    def get(self, request, *args, **kwargs):
        password_form = ProfilePasswordChangeForm(user=request.user)
        picture_form = ProfilePictureForm(instance=request.user.profile)
        ctx = {
            'form': password_form,
            'picture_form': picture_form,
            'user': request.user,
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        # If the Update Picture button was pressed
        if 'picture' in request.POST:
            picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
            if picture_form.is_valid():
                picture_form.save()
                ctx = {
                    'form': ProfilePasswordChangeForm(user=request.user),
                    'picture_form': ProfilePictureForm(instance=request.user.profile),
                    'user': request.user,
                    'picture_success': True,
                }
                return self.render_to_response(ctx)
            else:
                ctx = {
                    'form': ProfilePasswordChangeForm(user=request.user),
                    'picture_form': picture_form,
                    'user': request.user,
                }
                return self.render_to_response(ctx)

        # If the Change Password button was pressed
        password_form = ProfilePasswordChangeForm(user=request.user, data=request.POST)
        picture_form = ProfilePictureForm(instance=request.user.profile)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect(self.success_url)
        else:
            ctx = {
                'form': password_form,
                'picture_form': picture_form,
                'user': request.user,
            }
            return self.render_to_response(ctx)

    def render_to_response(self, context):
        from django.shortcuts import render
        return render(self.request, self.template_name, context)
