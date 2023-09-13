from django.shortcuts import render

# Create your views here.
def image_index(request):
    return render(request, 'editimage.html')
