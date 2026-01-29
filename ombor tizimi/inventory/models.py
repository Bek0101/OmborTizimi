"""Models for Inventory Management System."""
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone


class Category(models.Model):
    """Product Category model."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model for inventory tracking."""
    
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilogram'),
        ('liter', 'Liter'),
        ('meter', 'Meter'),
        ('box', 'Box'),
        ('pack', 'Pack'),
    ]

    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU/Code")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    minimum_stock = models.IntegerField(default=10, help_text="Alert when stock falls below this")
    reorder_quantity = models.IntegerField(default=50, help_text="Suggested quantity to reorder")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def current_stock(self):
        """Calculate current stock from transactions."""
        stock_in = StockTransaction.objects.filter(
            product=self,
            transaction_type='IN'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        stock_out = StockTransaction.objects.filter(
            product=self,
            transaction_type='OUT'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        return stock_in - stock_out

    @property
    def is_low_stock(self):
        """Check if current stock is below minimum."""
        return self.current_stock < self.minimum_stock

    @property
    def stock_status(self):
        """Return stock status."""
        if self.current_stock <= 0:
            return 'OUT_OF_STOCK'
        elif self.is_low_stock:
            return 'LOW_STOCK'
        return 'IN_STOCK'


class StockTransaction(models.Model):
    """Model to track all stock movements."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    TRANSACTION_REASON_CHOICES = [
        # Stock IN reasons
        ('purchase', 'Purchase'),
        ('return', 'Customer Return'),
        ('adjustment', 'Stock Adjustment'),
        ('donation', 'Donation'),
        ('transfer_in', 'Transfer In'),
        
        # Stock OUT reasons
        ('sale', 'Sale'),
        ('damage', 'Damage'),
        ('loss', 'Loss/Missing'),
        ('usage', 'Usage/Consumption'),
        ('transfer_out', 'Transfer Out'),
        ('return_vendor', 'Vendor Return'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=50, choices=TRANSACTION_REASON_CHOICES)
    
    reference_no = models.CharField(max_length=100, blank=True, null=True, help_text="Invoice/PO number")
    notes = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'created_at']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.product.sku} - {self.transaction_type} ({self.quantity}) on {self.created_at.date()}"

    def save(self, *args, **kwargs):
        """Validate before saving."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        super().save(*args, **kwargs)


class AuditLog(models.Model):
    """Model to track all system activities."""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_display = models.CharField(max_length=255, blank=True)
    
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} at {self.timestamp}"


class LowStockAlert(models.Model):
    """Model to store low stock alert history."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    current_stock = models.PositiveIntegerField()
    minimum_stock = models.PositiveIntegerField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Alert: {self.product.name} - Stock: {self.current_stock}"
