"""URL Configuration for Inventory app."""
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Products
    path('products/', views.products_list, name='products_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # Stock Transactions
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/create/', views.stock_transaction, name='stock_transaction'),

    # Alerts
    path('alerts/', views.low_stock_alerts, name='low_stock_alerts'),

    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/create/', views.create_category, name='create_category'),

    # Export
    path('export/products/', views.export_products, name='export_products'),
    path('export/transactions/', views.export_transactions, name='export_transactions'),
]
