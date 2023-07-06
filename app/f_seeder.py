from django.contrib.auth import get_user_model

User = get_user_model()

admin = User.objects.create_superuser('admin', 'Hero Staff', 'pass')
admin.save()
