from django.urls import path
from .views import CatchListView, CatchCreateView, RegisterView, lookup_admin

urlpatterns = [
    path('', CatchListView.as_view(), name='catch_list'),
    path('new/', CatchCreateView.as_view(), name='catch_new'),
    path('register/', RegisterView.as_view(), name='register'),
    path('lookups/', lookup_admin, name='lookup_admin'),
]
