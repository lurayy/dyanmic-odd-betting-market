from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def render_frontend(request):
    return render(request, 'index.html')


api_version_1 = [
    path('users/', include('users.urls')),
    path('markets/', include('market.urls')),
]

urlpatterns = [
    path('api/', include(api_version_1)),
    path('admin/', admin.site.urls),
    path('markets/', include('market.view_urls')),
    path('', render_frontend)
]
