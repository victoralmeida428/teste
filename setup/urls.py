from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.user.urls')),
    path('', include('apps.pdf.urls')),
    path('', include('apps.editimage.urls')),
    path('', include('apps.editvideo.urls')),
    path('', include('apps.geoloc.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
