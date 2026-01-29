# Inventory Management System (IMS)

A professional, production-ready web-based Inventory Management System built with Django and Bootstrap for small businesses.

## Features

### Core Features (MVP)
✅ **User Authentication & Authorization**
- Admin, Staff, and Viewer roles
- Secure password hashing
- Session-based authentication
- Role-based access control

✅ **Product Management (CRUD)**
- Create, Read, Update, Delete products
- Product fields: name, SKU, category, unit, minimum stock, price
- Image support for products
- Product categorization

✅ **Stock Transactions**
- Record Stock IN (Purchase, Return, Adjustment, Donation, Transfer In)
- Record Stock OUT (Sale, Damage, Loss, Usage, Transfer Out, Return to Vendor)
- Real-time stock calculation
- Transaction history tracking
- Reference number and notes support

✅ **Automatic Stock Calculation**
- Current stock = Total IN - Total OUT
- Real-time quantity updates
- Prevents manual stock editing

✅ **Low Stock Alerts**
- Automatic alert generation when stock < minimum
- Visual highlighting of low stock items
- Alert status tracking (Active, Resolved, Ignored)
- Dashboard alert display

✅ **Dashboard Analytics**
- Total active products count
- Low stock items count
- Today's stock IN/OUT summary
- Recent transactions feed
- Top moved products
- Real-time statistics

✅ **CSV Export**
- Export product list with all details
- Export transaction history with date filtering
- Audit trail for exports

### MVP Plus Features (Implemented)
✅ **Product Categories Management** - Create and manage product categories
✅ **Search & Filter** - Advanced filtering by category, status, and search by name/SKU
✅ **Audit Logs** - Complete audit trail of all system activities
✅ **Basic Analytics** - Most moved products, transaction trends
✅ **User Management** - Admin can create, manage, and delete users
✅ **Professional UI** - Responsive Bootstrap 5 interface

## Technology Stack

### Backend
- **Framework**: Django 4.2.8
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **REST Framework**: Django REST Framework 3.14.0
- **Authentication**: Django Session Authentication
- **Validation**: Django Built-in validators

### Frontend
- **HTML5 + Bootstrap 5.3.0**
- **Responsive Design** - Mobile, Tablet, Desktop
- **Font Awesome Icons** - Bootstrap Icons
- **CSS Grid & Flexbox** - Modern layout

### Additional Libraries
- Django CORS Headers
- Django Filter
- Python Decouple (Environment variables)
- Pillow (Image processing)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment (recommended)

### Step 1: Clone/Download the Project
```bash
cd "ombor tizimi"
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create admin account.

Or use the demo account:
- **Username**: admin
- **Password**: admin123

### Step 6: Create Demo Data (Optional)
```bash
python manage.py shell < setup_demo_data.py
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

## Demo Credentials

### Admin Account
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator (Full Access)

### Staff Account (Optional)
- **Username**: staff
- **Password**: staff123
- **Role**: Staff (Can record transactions)

## Usage Guide

### For Administrators

#### 1. User Management
- Navigate to **Users** section
- Create new user accounts
- Assign roles (Admin, Staff, Viewer)
- Delete inactive users

#### 2. Product Management
- Go to **Products** → **Add Product**
- Fill in product details (SKU, Name, Category, Unit, etc.)
- Set minimum stock level for alerts
- Upload product image (optional)
- Edit or delete products as needed

#### 3. Category Management
- Go to **Categories** → **Add Category**
- Organize products by category
- Manage category details

#### 4. Stock Operations
- Go to **Record Transaction**
- Select product and transaction type (IN/OUT)
- Select reason and enter quantity
- Add reference number (PO/Invoice) and notes
- Transaction is recorded with timestamp and user

#### 5. Monitoring
- View **Dashboard** for overview
- Check **Alerts** for low stock items
- Review **Transaction History** for audit trail

#### 6. Reporting
- Export **Products** list to CSV
- Export **Transactions** with date filtering
- Use filters for detailed analysis

### For Staff Members
- **Can**: Record stock transactions, view products, view transactions
- **Cannot**: Create/edit products, manage users, delete data

### For Viewers
- **Can**: View products, view dashboard, view transactions
- **Cannot**: Record transactions or make any changes

## Database Schema

### Core Models

#### Product
```python
- sku: CharField (Unique)
- name: CharField
- description: TextField
- category: ForeignKey(Category)
- unit: CharField (choices: pcs, kg, liter, meter, box, pack)
- minimum_stock: IntegerField
- reorder_quantity: IntegerField
- price: DecimalField
- image: ImageField
- is_active: BooleanField
- created_by: ForeignKey(User)
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### StockTransaction
```python
- product: ForeignKey(Product)
- transaction_type: CharField (IN/OUT)
- quantity: PositiveIntegerField
- reason: CharField (choices: purchase, sale, damage, etc.)
- reference_no: CharField (optional)
- notes: TextField (optional)
- created_by: ForeignKey(User)
- created_at: DateTimeField
```

#### Category
```python
- name: CharField (Unique)
- description: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### UserProfile
```python
- user: OneToOneField(User)
- role: CharField (admin, staff, viewer)
- department: CharField
- phone: CharField
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### AuditLog
```python
- user: ForeignKey(User)
- action: CharField (create, update, delete, export, login, logout)
- model_name: CharField
- object_id: PositiveIntegerField
- old_values: JSONField
- new_values: JSONField
- timestamp: DateTimeField
```

## Key Features Explained

### 1. Real-Time Stock Calculation
Stock is **never edited directly**. Instead, it's calculated from all transactions:
```
Current Stock = SUM(IN transactions) - SUM(OUT transactions)
```

### 2. Low Stock Alerts
When a transaction causes stock to fall below the minimum level:
- An alert is automatically created
- The product appears in red on the product list
- An alert card appears on the dashboard
- Admins can resolve the alert

### 3. Audit Trail
Every action is logged:
- Who performed the action
- What action was performed
- When it was performed
- What changed (old vs new values)

### 4. Role-Based Access Control (RBAC)
- **Admin**: Full access to all features
- **Staff**: Can record transactions and view data
- **Viewer**: Read-only access to dashboard and reports

## Security Features

✅ **Password Hashing** - Django's PBKDF2 algorithm
✅ **CSRF Protection** - Cross-Site Request Forgery tokens
✅ **SQL Injection Prevention** - Django ORM parameterized queries
✅ **XSS Protection** - Template auto-escaping
✅ **Session Security** - Secure session handling
✅ **Permission Checks** - View-level access control decorators

## API Endpoints (Built-in Django Admin)

- `/admin/` - Django Admin Interface
- All data accessible and manageable through admin

## Troubleshooting

### Issue: Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Issue: Database errors after migration
```bash
python manage.py migrate --run-syncdb
```

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Permission denied errors
Ensure proper user role is assigned:
```bash
python manage.py shell
# Then in Python:
from accounts.models import UserProfile
user = User.objects.get(username='username')
user.profile.role = 'admin'
user.profile.save()
```

## Production Deployment

### Before Going Live
1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set a strong `SECRET_KEY`
5. Use environment variables for sensitive data
6. Run `python manage.py collectstatic`
7. Set up HTTPS/SSL

### Recommended Production Stack
- **Web Server**: Gunicorn or uWSGI
- **Database**: PostgreSQL
- **Reverse Proxy**: Nginx
- **Process Manager**: Supervisor or systemd
- **Cache**: Redis (optional)

## File Structure

```
ombor tizimi/
├── config/              # Project configuration
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # WSGI application
│   └── asgi.py         # ASGI application
│
├── inventory/           # Main app
│   ├── models.py       # Data models
│   ├── views.py        # View logic
│   ├── forms.py        # Form definitions
│   ├── urls.py         # App URLs
│   ├── admin.py        # Admin configuration
│   └── signals.py      # Django signals
│
├── accounts/           # Authentication app
│   ├── models.py       # User profile model
│   ├── views.py        # Auth views
│   ├── forms.py        # Auth forms
│   └── urls.py         # Auth URLs
│
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── accounts/       # Auth templates
│   └── inventory/      # App templates
│
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Future Enhancements

- [ ] Mobile app (React Native / Flutter)
- [ ] Multi-warehouse support
- [ ] Advanced reporting & analytics
- [ ] Barcode scanning integration
- [ ] Email notifications for alerts
- [ ] Dashboard customization
- [ ] Advanced permission system
- [ ] API for third-party integration
- [ ] Automated reorder system
- [ ] Supplier management

## Support & Contact

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Contact system administrator

## License

© 2026 Inventory Management System. All rights reserved.

---

**Version**: 1.0.0  
**Last Updated**: January 28, 2026  
**Developed for**: University Co-work Program (Level 2 Upgrade)
#   o m b o r - t i z i m i - i m s  
 