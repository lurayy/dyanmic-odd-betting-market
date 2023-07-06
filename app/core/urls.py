from django.contrib import admin
from django.urls import path, include

api_version_1 = [path('users/', include('users.urls'))]

urlpatterns = [
    path('api/v1/', include(api_version_1)),
    path('', admin.site.urls),
]
