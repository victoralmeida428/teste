from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from apps.geoloc.forms import ExcelInput
from apps.geoloc.dash import Mapa
import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.utils.safestring import mark_safe
# Create your views here.

class RedirectLogin(RedirectView):
    url = reverse_lazy('login')
    def get(self, request, *args, **kwargs):
        msg = "<p>Faça login para continuar</p><p>ou cadastre-se clicando <a href='cadastro'>aqui</a></p>"
        messages.error(request, mark_safe(msg))
        return super().get(request, *args, **kwargs)

class GeoLoc(LoginRequiredMixin, FormView):
    template_name = "geoloc.html"
    form_class = ExcelInput
    success_url = "geoloc"


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(GeoLoc, self).get_context_data(**kwargs)
        context['button'] = 'Localizar Endereço'
        if kwargs.get('mapa'):
            context['mapa'] = kwargs.get('mapa')
        return context
    
    def form_valid(self, form: Any) -> HttpResponse:
        df = pd.DataFrame({'CEP':['0000000']})
        col = 'CEP'
        file = self.request.FILES.getlist('files')[0]
        col = form.cleaned_data['busca']
        df = pd.read_excel(file)
        try:
            mapa = Mapa(df, col).criar_mapa()
            return super().get(self.request, mapa)
        except:
            messages.error(self.request, 'Coluna não encontrada no arquivo')
            return redirect('geoloc')


    

        
