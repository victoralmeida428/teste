from apps.editvideo.views import *
from django.urls import path

urlpatterns = [
    path('video', VideoIndex.as_view(), name='video'),
]
