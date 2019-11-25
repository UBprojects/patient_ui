from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from website.models import *


@login_required
def dashboard(request):
    categories = CategoryPriority.objects.filter(auth_user_id=request.user.id).order_by('order')
    if not categories.exists():
        categories = Category.objects.all().order_by('id')
    else:
        exclude_cat_ids = categories.values_list('category_id', flat=True)
        remaining_cats = Category.objects.exclude(id__in=exclude_cat_ids).order_by('id')
        if remaining_cats.exists():
            new_list = list()
            for cat_priority in categories:
                new_list.append(cat_priority.category)
            for rem_cat in remaining_cats:
                new_list.append(rem_cat)
            categories = new_list.copy()

    result_list = list()
    for cat in categories:
        subcategories = SubCategory.objects.filter(category_id=cat.id).order_by('id')
        tmp_dict = {cat.title: list()}
        for subcat in subcategories:
            tmp_dict[cat.title].append({'title': subcat.title})
        result_list.append(tmp_dict)

    context_data = {'metadata': {'title': 'Dashboard'},
                    'result_list': result_list}
    return render(request, 'patient_ui/app/dashboard.html', context=context_data)
