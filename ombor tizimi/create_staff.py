import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

if not User.objects.filter(username='staff').exists():
    user = User.objects.create_user('staff', 'staff@example.com', 'staff123')
    user.is_staff = True
    user.save()
    UserProfile.objects.get_or_create(user=user, defaults={'role': 'staff'})
    print('✓ Staff foydalanuvchisi yaratildi: staff / staff123')
else:
    print('✓ Staff foydalanuvchisi allaqachon mavjud: staff / staff123')
