from django.urls import path
from .views import CatchListView, CatchCreateView, RegisterView, lookup_admin
from .views import CatchDetailView
from .views_rules import RulesView

urlpatterns = [
    path('', CatchListView.as_view(), name='catch_list'),
    path('new/', CatchCreateView.as_view(), name='catch_new'),
    path('<int:pk>/', CatchDetailView.as_view(), name='catch_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('lookups/', lookup_admin, name='lookup_admin'),
    path('rules/', RulesView.as_view(), name='rules'),
]
