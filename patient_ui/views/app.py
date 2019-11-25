from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from helpers import common
from website.models import *


@login_required
def dashboard(request):
    categories = CategoryPriority.objects.filter(auth_user_id=request.user.id).order_by('order')
    if not categories.exists():
        categories = Category.objects.all().order_by('id')

    result_list = list()
    for cat in categories:
        subcategories = SubCategory.objects.filter(category=cat).order_by('id')
        tmp_dict = {cat.title: list()}
        for subcat in subcategories:
            tmp_dict[cat.title].append({'title': subcat.title})
        result_list.append(tmp_dict)

    context_data = {'metadata': {'title': 'Dashboard'},
                    'result_list': result_list}
    return render(request, 'patient_ui/app/dashboard.html', context=context_data)
