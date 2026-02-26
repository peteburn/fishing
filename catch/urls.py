from django.urls import path
from .views import CatchListView, CatchCreateView, RegisterView

urlpatterns = [
    path('', CatchListView.as_view(), name='catch_list'),
    path('new/', CatchCreateView.as_view(), name='catch_new'),
    path('register/', RegisterView.as_view(), name='register'),
]
