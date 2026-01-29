"""
Setup script to create demo data for testing.
Run with: python manage.py shell < setup_demo_data.py
"""

from django.contrib.auth.models import User
from inventory.models import Category, Product, StockTransaction
from datetime import timedelta
from django.utils import timezone

# Create demo admin user if not exists
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    admin.first_name = 'Admin'
    admin.last_name = 'User'
    admin.save()
    print("✓ Created admin user")

# Create demo staff user
if not User.objects.filter(username='staff').exists():
    staff = User.objects.create_user('staff', 'staff@example.com', 'staff123')
    staff.first_name = 'Staff'
    staff.last_name = 'Member'
    staff.save()
    staff.profile.role = 'staff'
    staff.profile.save()
    print("✓ Created staff user")

# Create categories
categories = [
    ('Electronics', 'Electronic devices and components'),
    ('Textiles', 'Cloth, fabric, and textile materials'),
    ('Groceries', 'Food and grocery items'),
    ('Hardware', 'Tools and hardware supplies'),
    ('Office Supplies', 'Stationery and office materials'),
]

category_objects = {}
for name, desc in categories:
    cat, created = Category.objects.get_or_create(
        name=name,
        defaults={'description': desc}
    )
    category_objects[name] = cat
    if created:
        print(f"✓ Created category: {name}")

# Create sample products
products_data = [
    {
        'sku': 'ELEC-001',
        'name': 'USB Type-C Cable',
        'category': 'Electronics',
        'unit': 'pcs',
        'minimum_stock': 50,
        'reorder_quantity': 200,
        'price': 5.99,
    },
    {
        'sku': 'ELEC-002',
        'name': 'Wireless Mouse',
        'category': 'Electronics',
        'unit': 'pcs',
        'minimum_stock': 20,
        'reorder_quantity': 100,
        'price': 15.99,
    },
    {
        'sku': 'TEXT-001',
        'name': 'Cotton Fabric (1m)',
        'category': 'Textiles',
        'unit': 'meter',
        'minimum_stock': 30,
        'reorder_quantity': 150,
        'price': 8.50,
    },
    {
        'sku': 'GROC-001',
        'name': 'Organic Rice (10kg)',
        'category': 'Groceries',
        'unit': 'kg',
        'minimum_stock': 25,
        'reorder_quantity': 100,
        'price': 12.99,
    },
    {
        'sku': 'HARD-001',
        'name': 'Hammer (Steel)',
        'category': 'Hardware',
        'unit': 'pcs',
        'minimum_stock': 10,
        'reorder_quantity': 50,
        'price': 12.50,
    },
    {
        'sku': 'OFFICE-001',
        'name': 'A4 Paper (500 sheets)',
        'category': 'Office Supplies',
        'unit': 'pack',
        'minimum_stock': 20,
        'reorder_quantity': 100,
        'price': 4.99,
    },
]

admin_user = User.objects.get(username='admin')
staff_user = User.objects.get(username='staff')

product_objects = {}
for prod_data in products_data:
    category_name = prod_data.pop('category')
    prod, created = Product.objects.get_or_create(
        sku=prod_data['sku'],
        defaults={
            **prod_data,
            'category': category_objects[category_name],
            'created_by': admin_user,
        }
    )
    product_objects[prod_data['sku']] = prod
    if created:
        print(f"✓ Created product: {prod_data['sku']} - {prod_data['name']}")

# Create sample transactions
transactions_data = [
    ('ELEC-001', 'IN', 100, 'purchase', 'PO-2026-001', 'Initial stock purchase', admin_user),
    ('ELEC-001', 'OUT', 30, 'sale', 'INV-001', 'Sold to customer A', staff_user),
    ('ELEC-002', 'IN', 50, 'purchase', 'PO-2026-002', 'New shipment received', admin_user),
    ('TEXT-001', 'IN', 200, 'purchase', 'PO-2026-003', 'Fabric supplier delivery', admin_user),
    ('TEXT-001', 'OUT', 45, 'usage', '', 'Used in production', staff_user),
    ('GROC-001', 'IN', 150, 'purchase', 'PO-2026-004', 'Rice supplier', admin_user),
    ('GROC-001', 'OUT', 25, 'sale', 'INV-002', 'Sold to retailer', staff_user),
    ('HARD-001', 'IN', 50, 'purchase', 'PO-2026-005', 'Tools supplier', admin_user),
    ('HARD-001', 'OUT', 5, 'damage', '', 'Damaged during shipping', staff_user),
    ('OFFICE-001', 'IN', 100, 'purchase', 'PO-2026-006', 'Paper supplier', admin_user),
]

for sku, t_type, qty, reason, ref_no, notes, user in transactions_data:
    product = product_objects[sku]
    trans, created = StockTransaction.objects.get_or_create(
        product=product,
        transaction_type=t_type,
        quantity=qty,
        reason=reason,
        reference_no=ref_no,
        created_by=user,
        defaults={'notes': notes}
    )
    if created:
        print(f"✓ Created transaction: {sku} - {t_type} {qty}")

print("\n✓ Demo data setup completed successfully!")
print("\nDemo Credentials:")
print("Admin - Username: admin, Password: admin123")
print("Staff - Username: staff, Password: staff123")
