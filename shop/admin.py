from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'available', 'created']
    list_filter = ['category', 'available', 'created', 'updated']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'available']
    show_facets = admin.ShowFacets.ALWAYS
