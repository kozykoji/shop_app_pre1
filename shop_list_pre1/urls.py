from django.urls import path, include
from . import views
from shop_list_pre1.views import (
    IndexView, 
    ListDetailView, 
    BrandListView,
    BrandPostView,
    SearchView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('list/<int:pk>/', ListDetailView.as_view(), name='list_detail'),
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brand/<str:brand_slug>/', BrandPostView.as_view(), name='brand_post'),
    path('search/', SearchView.as_view(), name='search'),
    path('add/', views.add_shop, name='add_shop'),
    path('add_brand/', views.add_brand, name='add_brand'),
]