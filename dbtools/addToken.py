import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_shop.settings")

#django 1.6以下版本不需要写这个
import django
django.setup()

from user.models import User
from rest_framework.authtoken.models import Token

users=User.objects.all()
for user in users:     #  给user表里的每一位用户添加token
    Token.objects.get_or_create(user=user)







