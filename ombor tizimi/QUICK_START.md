# 🚀 QUICK REFERENCE GUIDE

## Starting the Application

### Windows Users
```bash
# Double-click this file in Explorer:
run.bat

# OR run from command line:
cd "ombor tizimi"
run.bat
```

### macOS/Linux Users
```bash
# Make executable (first time only):
chmod +x run.sh

# Run:
./run.sh

# OR:
bash run.sh
```

### Manual Start
```bash
# Activate environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

## 🌐 Access Points

| Resource | URL | Access |
|----------|-----|--------|
| Main App | http://localhost:8000 | All Users |
| Admin Panel | http://localhost:8000/admin/ | Admin Only |
| Dashboard | http://localhost:8000/ | All Users |
| Products | http://localhost:8000/products/ | All Users |
| Transactions | http://localhost:8000/transactions/ | All Users |
| Alerts | http://localhost:8000/alerts/ | All Users |

---

## 🔑 Demo Credentials

### Admin Account
```
Username: admin
Password: admin123
Role: Full Access
```

### Staff Account
```
Username: staff
Password: staff123
Role: Can record transactions
```

---

## 📌 Key Features Quick Access

### For Admins
1. **Dashboard** - Overview of inventory status
2. **Add Product** - Create new products
3. **Manage Users** - Create/delete user accounts
4. **Categories** - Organize products
5. **Export Data** - Download reports

### For Staff
1. **Dashboard** - View status
2. **Record Transaction** - Add stock IN/OUT
3. **View Products** - Search and filter
4. **View Alerts** - Check low stock items

### For Viewers
1. **Dashboard** - Read-only view
2. **Browse Products** - View all products
3. **View Transactions** - See history

---

## 🎯 Common Tasks

### Create a Product
1. Login as Admin
2. Click "New Product" in sidebar
3. Fill in product details
4. Set minimum stock level
5. Click "Create Product"

### Record Stock IN
1. Click "Record Transaction"
2. Select product
3. Select "Stock In" type
4. Enter quantity
5. Select reason (Purchase, Return, etc.)
6. Click "Record Transaction"

### Check Low Stock
1. Go to "Alerts" section
2. View all low stock products
3. Click product to see details
4. Record stock in if needed

### Export Data
1. Go to Products or Transactions
2. Click "Export CSV" button
3. Choose filters if needed
4. CSV file downloads automatically

---

## 🔍 File Locations

```
Project Root: ombor tizimi/

Important Files:
├── manage.py          # Django management
├── requirements.txt   # Python packages
├── README.md          # Full documentation
├── run.bat           # Windows launcher
├── run.sh            # Linux/Mac launcher

Directories:
├── config/           # Settings
├── inventory/        # Main app
├── accounts/         # Auth
├── templates/        # HTML files
├── static/          # CSS, JS
└── media/           # Uploads
```

---

## 🛠️ Troubleshooting

### Issue: "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### Issue: "ModuleNotFoundError"
```bash
# Reinstall packages
pip install -r requirements.txt
```

### Issue: Database errors
```bash
# Reset database
python manage.py migrate --run-syncdb
```

### Issue: Can't create admin
```bash
# Create manually
python manage.py createsuperuser
```

---

## 📊 System Architecture (Simple View)

```
User
 ↓
Login Form
 ↓
Django Auth
 ↓
Role Check (Admin/Staff/Viewer)
 ↓
Dashboard / Features
 ↓
Database (SQLite/PostgreSQL)
 ↓
Response to User
```

---

## 🔐 Security Quick Facts

✅ **Passwords**: Encrypted with PBKDF2
✅ **Session**: Secure browser cookies
✅ **CSRF**: Protection tokens on forms
✅ **Roles**: Admin, Staff, Viewer
✅ **Audit**: All actions logged
✅ **SQL**: Parameterized queries
✅ **XSS**: HTML auto-escaped

---

## 📱 Supported Browsers

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Mobile Safari (iOS 14+)
✅ Chrome Mobile (Android 8+)

---

## 🔄 Typical Workflows

### Morning Routine
1. Login to dashboard
2. Check alerts for low stock
3. Review overnight transactions
4. Record any new stock received

### During Day
1. Record sales/transactions
2. Monitor low stock items
3. Process purchase orders

### End of Day
1. Review all transactions
2. Check if reorders needed
3. Export daily report

---

## 💡 Tips & Best Practices

### For Admins
- ✅ Create users at month start
- ✅ Review audit logs weekly
- ✅ Set minimum stock realistically
- ✅ Export data regularly
- ✅ Keep product SKUs consistent

### For Staff
- ✅ Record transactions immediately
- ✅ Always add reference numbers
- ✅ Use clear descriptions
- ✅ Don't guess quantities
- ✅ Report discrepancies to admin

### For Viewers
- ✅ Check dashboard daily
- ✅ Export reports as needed
- ✅ Report issues to admin

---

## 📞 Support Checklist

Before contacting support:
- [ ] Check if Django is running
- [ ] Check if database is available
- [ ] Verify you're using correct credentials
- [ ] Try refreshing the page
- [ ] Check browser console for errors
- [ ] Verify internet connection
- [ ] Try different browser

---

## 🎓 Learning Resources

### For Django Development
- Django Official Docs: https://docs.djangoproject.com/
- Django for Beginners: https://djangoforbeginners.com/

### For Bootstrap
- Bootstrap Documentation: https://getbootstrap.com/docs/

### For SQL Databases
- Django ORM: https://docs.djangoproject.com/en/stable/topics/db/

---

## 📅 Maintenance Schedule

### Daily
- ✓ Monitor dashboard
- ✓ Process transactions
- ✓ Check alerts

### Weekly
- ✓ Review audit logs
- ✓ Check for low stock items
- ✓ Process purchase orders

### Monthly
- ✓ Export full report
- ✓ Review analytics
- ✓ Verify inventory accuracy

### Quarterly
- ✓ Back up database
- ✓ Review user accounts
- ✓ Update passwords

---

## ✅ Pre-Production Checklist

Before deploying to production:
- [ ] Set DEBUG = False
- [ ] Change SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Configure email settings
- [ ] Set up HTTPS/SSL
- [ ] Configure database (PostgreSQL)
- [ ] Set up backup strategy
- [ ] Test all features
- [ ] Train users
- [ ] Create documentation
- [ ] Set up monitoring
- [ ] Plan maintenance window

---

## 🎉 You're Ready!

The system is fully functional and ready to use.

**Next Steps:**
1. ✅ Run the application
2. ✅ Login with demo account
3. ✅ Create test products
4. ✅ Record test transactions
5. ✅ Explore all features
6. ✅ Invite users
7. ✅ Start using in production

---

**For detailed information, see: README.md**
**For technical details, see: IMPLEMENTATION_DETAILS.md**
**For project overview, see: PROJECT_SUMMARY.md**

---

*Version 1.0.0 | January 28, 2026 | Production Ready*
