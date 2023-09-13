from apps.editimage.views import *
from django.urls import path

urlpatterns = [
    path('image', image_index, name='image'),
]
