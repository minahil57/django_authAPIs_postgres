
from django.contrib import admin
from django.urls import path,include

from authAPIs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authAPIs.urls')),
]
