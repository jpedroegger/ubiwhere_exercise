from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/traffic/', include('traffic_monitor.api.urls')),
]
