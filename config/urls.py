from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



# This helper function allows serving media files in debug mode

urlpatterns = [
    # Standard Django Admin
    path('superadmin/', admin.site.urls),

    # Users Application Routes (e.g., /users/signin, /users/dashboard)
    path('users/', include('Users.urls')),
    
    # Admins Application Routes (e.g., /admins/signin, /admins/dashboard)
    path('admins/', include('Admins.urls')),
    
    # Default Route (You might want this to be the user sign-in page)
    path('', include('Users.urls')), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)