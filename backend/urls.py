from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Big Matrix Academy Admin Dashboard'
admin.site.index_title = 'Admin'
admin.site.site_title = 'Big Matrix Academy'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('categories.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('aggregated_api.urls')),
    path('api/', include('enrollments.urls')),
    path('api/', include('modules.urls')),
    path('api/', include('lessons.urls')),
    path('api/', include('payments.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)