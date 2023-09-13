from apps.pdf.views import *
from django.urls import path

urlpatterns = [
    path('merge', Merge.as_view(), name='merge'),
    path('excel', Excel.as_view(), name='excel'),
    path('word', Word.as_view(), name='word'),
    path('image', ImageFormView.as_view(), name='image'),
]
