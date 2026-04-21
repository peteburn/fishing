from django.urls import path
from .profile_views_split import PasswordChangeOnlyView, PictureUpdateOnlyView
from django.views.generic import TemplateView

urlpatterns = [
    path('password/', PasswordChangeOnlyView.as_view(), name='profile_password'),
    path('password/done/', TemplateView.as_view(template_name='catch/password_done.html'), name='profile_password_done'),
    path('picture/', PictureUpdateOnlyView.as_view(), name='profile_picture'),
    path('done/', TemplateView.as_view(template_name='catch/profile_done.html'), name='profile_edit_done'),
]
