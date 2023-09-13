from apps.geoloc.views import *
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(r'geoloc', GeoLoc.as_view(), name='geoloc'),
    path(r'login/', RedirectLogin.as_view(), name='redirect')
]
