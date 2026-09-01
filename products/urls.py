# from django.urls import path
# from .views import CategoryListCreateView, ProductDetailView, ProductListCreateView

# urlpatterns = [
#     path('categories/', CategoryListCreateView.as_view(), name='categories-list-create'),
#     path('', ProductListCreateView.as_view(), name='products-list-create'),
#     path('<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
# ]

# urls for both API (JSON output for Apps) and HTML Templates (web pages)

from django.urls import path
from . import views, api_views

app_name = 'products'

urlpatterns = [
    # HTML Template Views (Web Browser)
    path('', views.product_list, name='product_list'),
    path('<uuid:pk>/', views.product_detail, name='product_detail'),

    # REST API Views (Postman / JSON)
    path('api/', api_views.ProductListCreateView.as_view(), name='products-list-create'),
    path('api/<uuid:pk>/', api_views.ProductDetailView.as_view(), name='product-detail'),
    path('api/categories/', api_views.CategoryListCreateView.as_view(), name='categories-list-create'),
]