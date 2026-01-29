"""Signals for Inventory app."""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import StockTransaction, Product, LowStockAlert, AuditLog


@receiver(post_save, sender=StockTransaction)
def check_low_stock(sender, instance, created, **kwargs):
    """Check if product stock falls below minimum after transaction."""
    if created:
        product = instance.product
        current_stock = product.current_stock

        if current_stock < product.minimum_stock:
            # Check if there's already an active alert
            existing_alert = LowStockAlert.objects.filter(
                product=product,
                status='active'
            ).first()

            if not existing_alert:
                LowStockAlert.objects.create(
                    product=product,
                    current_stock=current_stock,
                    minimum_stock=product.minimum_stock,
                    status='active'
                )
        else:
            # Mark any active alerts as resolved
            LowStockAlert.objects.filter(
                product=product,
                status='active'
            ).update(
                status='resolved',
                resolved_at=timezone.now()
            )


@receiver(post_save, sender=Product)
def log_product_changes(sender, instance, created, **kwargs):
    """Log product creation/updates."""
    if created:
        AuditLog.objects.create(
            user=instance.created_by,
            action='create',
            model_name='Product',
            object_id=instance.id,
            object_display=str(instance),
            new_values={
                'sku': instance.sku,
                'name': instance.name,
                'category': instance.category.name if instance.category else None,
            }
        )


__all__ = []
