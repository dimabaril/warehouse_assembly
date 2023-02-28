from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
