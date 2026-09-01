# from rest_framework import generics, permissions
# from .models import Category, Product
# from .serializers import CategorySerializer, ProductSerializer

# class CategoryListCreateView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]  # Public view
#         return [permissions.IsAdminUser()]  # Only Admins can add items


# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.filter(is_active=True)
#     serializer_class = ProductSerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]  # Public view
#         return [permissions.IsAdminUser()]  # Only Admins can add items

# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'  # This tells Django to look up using the ID (Primary Key)

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         return [permissions.IsAdminUser()]  # Only Admins can edit/delete


# Views template-rendering functions For Ordinary Django

from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {
        'product': product,
    })