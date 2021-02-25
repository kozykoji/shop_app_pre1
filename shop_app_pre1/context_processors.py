from django.db.models import Count

from shop_list_pre1.models import Brand


def common(request):
    context = {
        'treatbrands': Brand.objects.annotate(num_posts=Count('取扱ブランド'))
    }
    return context