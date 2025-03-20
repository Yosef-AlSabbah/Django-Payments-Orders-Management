from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class Product(TranslatableAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'available', 'created']
    list_filter = ['category', 'available', 'created', 'updated']
    search_fields = ['name', 'slug']
    list_editable = ['price', 'available']
    show_facets = admin.ShowFacets.ALWAYS

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
