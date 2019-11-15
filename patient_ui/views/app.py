from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    context_data = {'metadata': {'title': 'Dashboard'}}
    return render(request, 'patient_ui/app/dashboard.html', context=context_data)
