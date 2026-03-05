from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse
from django.views import View
import os

class RulesView(View):
    def get(self, request):
        prev = request.META.get('HTTP_REFERER', reverse('home'))
        rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'multi-species-2026.pdf')
        if os.path.exists(rules_path):
            return FileResponse(open(rules_path, 'rb'), content_type='application/pdf')
        return render(request, 'rules_not_found.html', {'prev': prev})
