from apps.user.views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('cadastro', Cadastro.as_view(), name='cadastro'),
    path('logout', logout, name='logout'),
    path('login', Login.as_view(), name='login'),
    path('account', AccountHomeView.as_view(), name='accounthome'),
    path('changepass', ChangePassword.as_view(), name='changepass'),
    path('perfil', PerfilView.as_view(), name='perfil'),
    path('ajuda', PixView.as_view(), name='ajuda'),
    path('pix/', PixGenerator.as_view(), name='pix'),
    path('forgot_password/', EsqueciSenha.as_view(), name='forgot_password'),
    path('forgot_password/pinconfirmation/', ConfirmarPin.as_view(), name='forgot_password2'),
    path('changepassword/', ChangeForgotPass.as_view(), name='forgot_password3'),

]
