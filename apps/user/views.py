from typing import Any, Dict, Optional
from django import http
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView, ListView
from django.contrib.auth.models import User
from apps.user.forms import *
from .models import PixImage
import numpy as np
from django.core.mail import send_mail


def index(request):
    return render(request, 'home/index.html')

class Login(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form) -> HttpResponse:
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.get(username=username)
        nome = user.get_full_name()
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        messages.success(self.request, f'Bem-Vindo, {nome.title()}')
        return super().form_valid(form)

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso')
    return redirect('index')

class Cadastro(FormView):
    template_name = "cadastro.html"
    form_class = CadastroForm
    success_url = "/"

    def form_valid(self, form) -> HttpResponse:
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        new_user = User(username=username,
                        password=password,
                        email=email,
                        first_name= first_name,
                        last_name=last_name)
        new_user.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        messages.success(self.request, f'Seja bem vindo, {first_name} {last_name}')
        return super().form_valid(form)

class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name='accounthome.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    
    def get_object(self):
        return self.request.user
    
    @method_decorator(login_required)
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
class ChangePassword(FormView):
    form_class = ChangePassowrdForm
    template_name = 'conta/alterasenha.html'
    success_url = 'account'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form: Any) -> HttpResponse:
        user = self.request.user
        password = form.cleaned_data.get('new_password2')
        user.set_password(password)
        user.save()
        return super().form_valid(form)
    
class PerfilView(LoginRequiredMixin, DetailView, FormView):
    model = User
    template_name = 'conta/perfil.html'
    form_class = PerfilForm
    success_url = 'account'

    @method_decorator(login_required)
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.get(username=self.get_object())
        return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form: Any) -> HttpResponse:
        self.object = self.get_queryset()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        self.object.first_name = first_name
        self.object.save()
        self.object.last_name = last_name
        self.object.save()
        messages.success(self.request, 'Dados Atualizados com Sucesso')
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        self.object = self.get_queryset()
        print(form.errors)
        return super().form_invalid(form)
    
class PixView(LoginRequiredMixin, FormView):
    form_class = PixForm
    success_url = 'pix'
    template_name = 'conta/ajuda.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form: Any) -> HttpResponse:
        self.data = form.cleaned_data
        return super().form_valid(form)

    def get_success_url(self) -> str:
        # Construa a URL de redirecionamento de sucesso com base nos dados do formulário
        # Utilize os dados do formulário para construir a URL
        # Por exemplo:
        data = self.data
        success_url = f"pix/?valor={data.get('doacao')}"
        return success_url

class PixGenerator(LoginRequiredMixin, ListView):
    template_name = 'conta/pix.html'
    model = PixImage

    def get_queryset(self):
        qs =  super().get_queryset()
        qs = qs.get(valor = self.request.GET.get('valor'))
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

email_pin = {}
class EsqueciSenha(FormView):
    template_name = 'recuperar_senha.html'
    form_class = ForgotPassForm
    success_url = 'pinconfirmation/?email='

    def form_valid(self, form: Any) -> HttpResponse:
        codigo = np.random.randint(100000,999999)
        email = form.cleaned_data.get('email')
        email_pin[email]=codigo
        send_mail('Recuperação da senha', f'Aqui está seu código {codigo}', 'master.edition.ltd@gmail.com',recipient_list=[email])
        self.success_url += email
        return super().form_valid(form)

class ConfirmarPin(FormView):
    template_name='recuperar_senha_2.html'
    form_class = PinConfirmedForm
    success_url = '/changepassword'

    def form_valid(self, form: Any) -> HttpResponse:
        email = self.request.GET.get('email')
        code = email_pin.get(email)
        if code != form.cleaned_data.get('pin'):
            messages.error(self.request, 'Código incorreto')
            self.success_url = f'pinconfirmation/?email={email}'
            return super().form_invalid(form)
        self.success_url += f'?email={email}&code={code}'
        return super().form_valid(form)

class ChangeForgotPass(FormView):
    template_name = 'recuperar_senha_3.html'
    form_class = ChangeForgotPassForm
    success_url = '/'

    def form_valid(self, form: Any) -> HttpResponse:
        email = self.request.GET.get('email')
        code_real = email_pin.get(email)
        code_get = self.request.GET.get('code')
        if not code_real:
            messages.error(self.request, f'Tempo Expirado')
            return redirect('login')
        if int(code_real) != int(code_get):
            messages.error(self.request, f'URL incorreta {code_get} (get) {code_real} (real)')
            return redirect('login')

        user = User.objects.get(email=email)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        nome = user.get_full_name()
        messages.success(self.request, f'Olá, {nome}, sua senha foi atualizada')
        user = auth.authenticate(username=user.username, password=password)
        auth.login(self.request, user)
        return super().form_valid(form)

    
