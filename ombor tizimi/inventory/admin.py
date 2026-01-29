"""Django Admin Configuration for Inventory Management System."""
from django.contrib import admin
from .models import Category, Product, StockTransaction, AuditLog, LowStockAlert
from accounts.models import UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'name', 'category', 'current_stock', 'minimum_stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['sku', 'name']
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'current_stock']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('sku', 'name', 'description', 'category', 'image')
        }),
        ('Stock Settings', {
            'fields': ('unit', 'minimum_stock', 'reorder_quantity')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at', 'current_stock'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'reason', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'reason', 'created_at']
    search_fields = ['product__name', 'product__sku', 'reference_no']
    readonly_fields = ['created_by', 'created_at']

    fieldsets = (
        ('Transaction Details', {
            'fields': ('product', 'transaction_type', 'quantity', 'reason')
        }),
        ('Additional Info', {
            'fields': ('reference_no', 'notes')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(LowStockAlert)
class LowStockAlertAdmin(admin.ModelAdmin):
    list_display = ['product', 'current_stock', 'minimum_stock', 'status', 'created_at', 'resolved_at']
    list_filter = ['status', 'created_at']
    search_fields = ['product__name', 'product__sku']
    readonly_fields = ['created_at', 'resolved_at', 'current_stock', 'minimum_stock']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name']
    readonly_fields = ['user', 'action', 'model_name', 'timestamp', 'old_values', 'new_values']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'department']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('department', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
