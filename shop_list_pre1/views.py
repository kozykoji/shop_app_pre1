from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from shop_list_pre1.models import List, Brand
from django.views import generic
from .forms import SearchForm, ListForm, BrandForm

# Create your views here.
class ListDetailView(DetailView):
    model = List
    template_name = 'list_detail.html'


class IndexView(ListView):
    model = List
    template_name = 'index.html'

class BrandListView(ListView):
    model = Brand
    template_name = 'brand_list.html'
    queryset = Brand.objects.annotate(num_posts=Count('取扱ブランド'))

class BrandPostView(ListView):
    model = List
    template_name = 'brand_post.html'

    def get_queryset(self):
        brand_slug = self.kwargs['brand_slug']
        self.brand = get_object_or_404(Brand, slug=brand_slug)
        qs = super().get_queryset().filter(treatbrands=self.brand)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = self.brand
        return context

class SearchView(generic.ListView):
    paginate_by = 5
    template_name = 'search.html'
    model = List
    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('shopname', None),
            self.request.POST.get('treatbrands', None),
            self.request.POST.get('treatused', None),
            self.request.POST.get('genre', None),
            self.request.POST.get('address', None),
        ]
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        shopname = ''
        treatbrands = ''
        treatused = ''
        genre = ''
        address = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            shopname = form_value[0]
            treatbrands = form_value[1]
            treatused = form_value[2]
            genre = form_value[3]
            address = form_value[4]
        default_data = {'shopname': shopname,  # タイトル
                        'treatbrands': treatbrands,  
                        'treatused': treatused,
                        'genre' : genre,
                        'address': address, # 内容
                        }
        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form
        return context
    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            shopname = form_value[0]
            treatbrands = form_value[1]
            treatused = form_value[2]
            genre = form_value[3]
            address = form_value[4]
            # 検索条件
            condition_shopname = Q()
            condition_treatbrands = Q()
            condition_treatused = Q()
            condition_genre = Q()
            condition_address = Q()
            if len(shopname) != 0 and shopname[0]:
                condition_shopname = Q(shopname__icontains=shopname)
            if len(treatbrands) != 0 and treatbrands[0]:
                condition_treatbrands = Q(treatbrands__brandname__contains=treatbrands)
            if len(treatused) != 0 and treatused[0]:
                condition_treatused = Q(treatused__contains=treatused)
            if len(genre) != 0 and genre[0]:
                condition_genre = Q(genre__contains=genre)
            if len(address) != 0 and address[0]:
                condition_address = Q(address__contains=address)
            return List.objects.select_related().filter(condition_shopname & condition_treatbrands & condition_treatused & condition_genre & condition_address)
        else:
            # 何も返さない
            return List.objects.none()

def add_shop(request):
    model = List.objects.values()
    form = ListForm(request.POST )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, 'add_shop.html', {'form': form})
    else:
        form = ListForm()
        return render(request, 'add_shop.html', {'form': form})

def add_brand(request):
    model = Brand.objects.values()
    form = BrandForm(request.POST )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("add_shop")
        else:
            return render(request, 'add_brand.html', {'form': form})
    else:
        form = BrandForm()
        return render(request, 'add_brand.html', {'form': form})

