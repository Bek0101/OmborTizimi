"""Views for Inventory app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count, F
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
import csv
from datetime import timedelta

from .models import Product, StockTransaction, Category, AuditLog, LowStockAlert
from .forms import (
    ProductForm, StockTransactionForm, CategoryForm,
    ProductFilterForm, TransactionFilterForm
)


def is_admin(user):
    """Check if user is admin."""
    return user.is_staff or (hasattr(user, 'profile') and user.profile.role == 'admin')


def is_staff_or_admin(user):
    """Check if user is staff or admin."""
    if hasattr(user, 'profile'):
        return user.profile.role in ['admin', 'staff']
    return user.is_staff


@login_required
@require_http_methods(["GET"])
def dashboard(request):
    """Main dashboard view."""
    # Calculate statistics
    total_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(transactions__transaction_type='IN') | Q(transactions__transaction_type='OUT')
    ).annotate(
        stock=Sum(
            F('transactions__quantity') * 
            (1 if F('transactions__transaction_type') == 'IN' else -1),
            output_field=models.IntegerField()
        )
    ).filter(stock__lt=F('minimum_stock')).count()

    # Today's transactions
    today = timezone.now().date()
    today_stock_in = StockTransaction.objects.filter(
        transaction_type='IN',
        created_at__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0

    today_stock_out = StockTransaction.objects.filter(
        transaction_type='OUT',
        created_at__date=today
    ).aggregate(total=Sum('quantity'))['total'] or 0

    # Low stock products for alerts
    low_stock_alerts = LowStockAlert.objects.filter(
        status='active'
    ).select_related('product')[:5]

    # Recent transactions
    recent_transactions = StockTransaction.objects.select_related(
        'product', 'created_by'
    ).order_by('-created_at')[:10]

    # Top products by movement
    top_products = StockTransaction.objects.values('product__name', 'product__sku').annotate(
        total_quantity=Sum('quantity'),
        total_transactions=Count('id')
    ).order_by('-total_quantity')[:5]

    context = {
        'page_title': 'Dashboard',
        'total_products': total_products,
        'low_stock_count': low_stock_products,
        'today_stock_in': today_stock_in,
        'today_stock_out': today_stock_out,
        'low_stock_alerts': low_stock_alerts,
        'recent_transactions': recent_transactions,
        'top_products': top_products,
    }

    return render(request, 'inventory/dashboard.html', context)


@login_required
@require_http_methods(["GET"])
def products_list(request):
    """List all products."""
    products = Product.objects.select_related('category').filter(is_active=True)

    # Apply filters
    form = ProductFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('category'):
            products = products.filter(category=form.cleaned_data['category'])

        if form.cleaned_data.get('search'):
            search = form.cleaned_data['search']
            products = products.filter(
                Q(name__icontains=search) | Q(sku__icontains=search)
            )

        status = form.cleaned_data.get('status')
        if status == 'low_stock':
            # Filter products with low stock
            products_list = []
            for product in products:
                if product.is_low_stock:
                    products_list.append(product)
            products = products_list
        elif status == 'out_of_stock':
            products_list = []
            for product in products:
                if product.current_stock <= 0:
                    products_list.append(product)
            products = products_list
        elif status == 'in_stock':
            products_list = []
            for product in products:
                if product.current_stock > 0 and not product.is_low_stock:
                    products_list.append(product)
            products = products_list

    context = {
        'page_title': 'Products',
        'products': products,
        'form': form,
        'can_edit': is_admin(request.user),
    }
    return render(request, 'inventory/products_list.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def create_product(request):
    """Create new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()

            # Log action
            AuditLog.objects.create(
                user=request.user,
                action='create',
                model_name='Product',
                object_id=product.id,
                object_display=str(product),
            )

            messages.success(request, f'Product {product.name} created successfully.')
            return redirect('product_detail', pk=product.id)
    else:
        form = ProductForm()

    context = {
        'page_title': 'Create Product',
        'form': form,
        'action': 'create'
    }
    return render(request, 'inventory/product_form.html', context)


@login_required
@require_http_methods(["GET"])
def product_detail(request, pk):
    """Product detail view."""
    product = get_object_or_404(Product, id=pk)
    transactions = product.transactions.select_related('created_by').order_by('-created_at')

    context = {
        'page_title': f'Product: {product.name}',
        'product': product,
        'transactions': transactions,
        'can_edit': is_admin(request.user),
    }
    return render(request, 'inventory/product_detail.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_product(request, pk):
    """Edit product."""
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Product',
                object_id=product.id,
                object_display=str(product),
            )

            messages.success(request, f'Product {product.name} updated successfully.')
            return redirect('product_detail', pk=product.id)
    else:
        form = ProductForm(instance=product)

    context = {
        'page_title': f'Edit: {product.name}',
        'form': form,
        'product': product,
        'action': 'edit'
    }
    return render(request, 'inventory/product_form.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_product(request, pk):
    """Delete product (soft delete)."""
    product = get_object_or_404(Product, id=pk)
    product_name = product.name
    product.is_active = False
    product.save()

    AuditLog.objects.create(
        user=request.user,
        action='delete',
        model_name='Product',
        object_id=product.id,
        object_display=product_name,
    )

    messages.success(request, f'Product {product_name} deleted successfully.')
    return redirect('products_list')


@login_required
@user_passes_test(is_staff_or_admin)
@require_http_methods(["GET", "POST"])
def stock_transaction(request):
    """Record stock transaction."""
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()

            AuditLog.objects.create(
                user=request.user,
                action='create',
                model_name='StockTransaction',
                object_id=transaction.id,
                object_display=str(transaction),
            )

            messages.success(request, 'Stock transaction recorded successfully.')
            return redirect('transactions_list')
    else:
        form = StockTransactionForm()

    context = {
        'page_title': 'Record Stock Transaction',
        'form': form,
    }
    return render(request, 'inventory/stock_transaction.html', context)


@login_required
@require_http_methods(["GET"])
def transactions_list(request):
    """List all transactions."""
    transactions = StockTransaction.objects.select_related(
        'product', 'created_by'
    ).order_by('-created_at')

    form = TransactionFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data.get('product'):
            transactions = transactions.filter(product=form.cleaned_data['product'])

        if form.cleaned_data.get('transaction_type'):
            transactions = transactions.filter(
                transaction_type=form.cleaned_data['transaction_type']
            )

        if form.cleaned_data.get('start_date'):
            transactions = transactions.filter(
                created_at__date__gte=form.cleaned_data['start_date']
            )

        if form.cleaned_data.get('end_date'):
            transactions = transactions.filter(
                created_at__date__lte=form.cleaned_data['end_date']
            )

    paginator_from = (request.GET.get('page', 1) - 1) * 50
    paginator_to = paginator_from + 50

    context = {
        'page_title': 'Stock Transactions',
        'transactions': transactions[paginator_from:paginator_to],
        'total_transactions': transactions.count(),
        'form': form,
    }
    return render(request, 'inventory/transactions_list.html', context)


@login_required
@require_http_methods(["GET"])
def low_stock_alerts(request):
    """View low stock alerts."""
    alerts = LowStockAlert.objects.select_related('product', 'resolved_by').filter(
        status='active'
    ).order_by('-created_at')

    context = {
        'page_title': 'Low Stock Alerts',
        'alerts': alerts,
    }
    return render(request, 'inventory/low_stock_alerts.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def categories(request):
    """Manage categories."""
    categories_list = Category.objects.all().order_by('name')

    if request.method == 'POST':
        action = request.POST.get('action')
        category_id = request.POST.get('category_id')

        if action == 'delete' and category_id:
            category = get_object_or_404(Category, id=category_id)
            category_name = category.name
            category.delete()
            messages.success(request, f'Category {category_name} deleted.')
            return redirect('categories')

    context = {
        'page_title': 'Categories',
        'categories': categories_list,
    }
    return render(request, 'inventory/categories.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def create_category(request):
    """Create category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category {category.name} created successfully.')
            return redirect('categories')
    else:
        form = CategoryForm()

    context = {
        'page_title': 'Create Category',
        'form': form,
    }
    return render(request, 'inventory/category_form.html', context)


@login_required
@require_http_methods(["GET"])
def export_products(request):
    """Export products to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['SKU', 'Name', 'Category', 'Unit', 'Current Stock', 'Minimum Stock', 'Price', 'Status'])

    products = Product.objects.select_related('category').filter(is_active=True)
    for product in products:
        writer.writerow([
            product.sku,
            product.name,
            product.category.name if product.category else '',
            product.unit,
            product.current_stock,
            product.minimum_stock,
            product.price,
            product.stock_status,
        ])

    AuditLog.objects.create(
        user=request.user,
        action='export',
        model_name='Product',
    )

    messages.success(request, 'Products exported successfully.')
    return response


@login_required
@require_http_methods(["GET"])
def export_transactions(request):
    """Export transactions to CSV."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Product SKU', 'Product Name', 'Type', 'Quantity', 'Reason', 'User', 'Reference'])

    transactions = StockTransaction.objects.select_related('product', 'created_by')

    if start_date:
        transactions = transactions.filter(created_at__date__gte=start_date)
    if end_date:
        transactions = transactions.filter(created_at__date__lte=end_date)

    for transaction in transactions.order_by('-created_at'):
        writer.writerow([
            transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            transaction.product.sku,
            transaction.product.name,
            transaction.transaction_type,
            transaction.quantity,
            transaction.get_reason_display(),
            transaction.created_by.get_full_name() or transaction.created_by.username,
            transaction.reference_no or '',
        ])

    AuditLog.objects.create(
        user=request.user,
        action='export',
        model_name='StockTransaction',
    )

    messages.success(request, 'Transactions exported successfully.')
    return response


from django.db import models
