from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse
from django.views import View
import os

class RulesView(View):
    def get(self, request):
        prev = request.META.get('HTTP_REFERER', reverse('home'))
        rules_path = '/home/pete/Documents/multi-species-2026.pdf'
        if os.path.exists(rules_path):
            return FileResponse(open(rules_path, 'rb'), content_type='application/pdf')
        return render(request, 'rules_not_found.html', {'prev': prev})
