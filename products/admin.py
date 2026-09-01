from django.contrib import admin

from products.models import Category, Product

# Register your models here.
# admin.site.register(Category)

# admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'stock')
    search_fields = ('title', 'description')
    list_filter = ('category', 'is_active')
    ordering = ('title',)
