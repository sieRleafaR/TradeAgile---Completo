from django import forms  # Importa o módulo de formulários do Django
from django.contrib.auth.models import User  # Importa o modelo de usuário padrão do Django
from django.contrib.auth.forms import UserCreationForm  # Importa o formulário de criação de usuário padrão do Django
from . import models

# Formulário de registro de usuário, estendendo o formulário de criação de usuário do Django
class UserRegisterForm(UserCreationForm):
    # Adiciona um campo de e-mail obrigatório com mensagens de erro personalizadas
    email = forms.EmailField(required=True, error_messages={
        'required': 'Este campo é obrigatório.',
        'invalid': 'Por favor, insira um endereço de e-mail válido.'
    })

    class Meta:
        model = User  # Especifica que o modelo associado é o modelo de usuário padrão do Django
        fields = ['username', 'email', 'password1', 'password2']  # Define os campos que serão exibidos no formulário

# Formulário para o modelo de Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente  # Especifica que o modelo associado é o modelo de Cliente
        fields = '__all__'  # Inclui todos os campos do modelo no formulário
class FornecedorForm(forms.ModelForm):
    class Meta:
        model = models.Fornecedor  # Especifica que o modelo associado é o modelo de Cliente
        fields = '__all__'  # Inclui todos os campos do modelo no formulário
class VendedorForm(forms.ModelForm):
    class Meta:
        model = models.Vendedor  # Especifica que o modelo associado é o modelo de Cliente
        fields = '__all__'  # Inclui todos os campos do modelo no formulário
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = models.Produto  # Especifica que o modelo associado é o modelo de Cliente
        fields = '__all__'  # Inclui todos os campos do modelo no formulário
