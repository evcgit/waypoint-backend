"""
URL configuration for waypoint_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from views import index_view
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework_simplejwt.views import TokenVerifyView
from django.http import JsonResponse
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trips.urls')),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
    path('auth/token/verify/', csrf_exempt(TokenVerifyView.as_view()), name='token_verify'),
    
    # Static files and assets
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.VITE_APP_DIR / 'dist/assets'}),
    
    # Catch all route should be LAST
    re_path(r'^.*$', index_view, name='index'),
]
