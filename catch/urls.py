from django.urls import path
from .views import CatchListView, CatchCreateView, RegisterView, lookup_admin
from .views import CatchDetailView, CatchUpdateView, CatchDeleteView
from .views_rules import RulesView

urlpatterns = [
    path('', CatchListView.as_view(), name='catch_list'),
    path('new/', CatchCreateView.as_view(), name='catch_new'),
    path('<int:pk>/', CatchDetailView.as_view(), name='catch_detail'),
    path('<int:pk>/edit/', CatchUpdateView.as_view(), name='catch_edit'),
    path('<int:pk>/delete/', CatchDeleteView.as_view(), name='catch_delete'),
    path('register/', RegisterView.as_view(), name='register'),
    path('lookups/', lookup_admin, name='lookup_admin'),
    path('rules/', RulesView.as_view(), name='rules'),
]
