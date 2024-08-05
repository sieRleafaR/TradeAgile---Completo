from django.shortcuts import render, redirect  # Importa as funções 'render' e 'redirect' do Django para renderização e redirecionamento de páginas
from .models import Produto, Venda, ItensVenda, Cliente, Fornecedor, Vendedor  # Importa os modelos da aplicação atual
from .forms import UserRegisterForm, ClienteForm, FornecedorForm, VendedorForm, ProdutoForm  # Importa os formulários personalizados da aplicação atual
from django.contrib.auth import authenticate, login  # Importa funções de autenticação e login do Django
from django.contrib.auth.forms import AuthenticationForm  # Importa o formulário de autenticação padrão do Django
from django.contrib import messages  # Importa a biblioteca de mensagens do Django para feedbacks ao usuário
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cliente, Produto, Vendedor, Venda, ItensVenda

# Função para renderizar a página inicial
def home(request):
    return render(request, 'trade/home.html')
def cadastros_view(request):
    return render(request, 'trade/cadastros.html')

# Função para o cadastro de clientes
def cadastro_clientes(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa o formulário
        form = ClienteForm(request.POST)
        if form.is_valid():  # Se o formulário for válido, salva os dados e redireciona para a página inicial
            form.save()
            return redirect('cadastros')
    else:  # Se o método de requisição não for POST, exibe um formulário vazio
        form = ClienteForm()
    return render(request, 'trade/cadastro_clientes.html', {'form': form})# Função para o cadastro de clientes


def cadastro_prod(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa o formulário
        form = ProdutoForm(request.POST)
        if form.is_valid():  # Se o formulário for válido, salva os dados e redireciona para a página inicial
            form.save()
            return redirect('cadastros')
    else:  # Se o método de requisição não for POST, exibe um formulário vazio
        form = ProdutoForm()
    return render(request, 'trade/cadastro_produtos.html', {'form': form})# Função para o cadastro de clientes


def cadastro_vend(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa o formulário
        form = VendedorForm(request.POST)
        if form.is_valid():  # Se o formulário for válido, salva os dados e redireciona para a página inicial
            form.save()
            return redirect('cadastros')
    else:  # Se o método de requisição não for POST, exibe um formulário vazio
        form = VendedorForm()
    return render(request, 'trade/cadastro_vendedor.html', {'form': form})# Função para o cadastro de clientes


def cadastro_forn(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa o formulário
        form = FornecedorForm(request.POST)
        if form.is_valid():  # Se o formulário for válido, salva os dados e redireciona para a página inicial
            form.save()
            return redirect('cadastros')
    else:  # Se o método de requisição não for POST, exibe um formulário vazio
        form = FornecedorForm()
    return render(request, 'trade/cadastro_fornecedor.html', {'form': form})



# Função para exibir tabelas de dados de clientes, fornecedores, produtos e vendas
def demonstrativo_tabelas(request):
    clientes = Cliente.objects.all()
    fornecedores = Fornecedor.objects.all()
    produtos = Produto.objects.all()
    vendas = Venda.objects.all()
    return render(request, 'trade/demonstrativo_tabelas.html', {
        'clientes': clientes,
        'fornecedores': fornecedores,
        'produtos': produtos,
        'vendas': vendas,
    })

# Função para exibir a galeria de produtos
def galeria_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'trade/galeria_produtos.html', {'produtos': produtos})

# Função para processar a realização de uma venda
def realizar_venda(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa os dados da venda
        cliente_id = request.POST.get('cliente')
        produto_id = request.POST.get('produto')
        quantidade = int(request.POST.get('quantidade'))  # Certifique-se de converter a quantidade para int
        cliente = Cliente.objects.get(idcli=cliente_id)
        produto = Produto.objects.get(idprod=produto_id)
        vendedor = Vendedor.objects.first()  # Supondo que há um vendedor padrão
        fornecedor = produto.idforn

        # Verifica se a quantidade solicitada está disponível em estoque
        estoque_disponivel = int(produto.situprod)
        if quantidade > estoque_disponivel:
            messages.error(request, f"Estoque atual de {estoque_disponivel} excedido.")
            return redirect('realizar_venda')  # Redireciona para a mesma página

        # Calcula o valor da venda
        valor_venda = produto.valorprod * quantidade
        venda = Venda.objects.create(
            codivend='12345',  # Código de venda gerado automaticamente
            idcli=cliente,
            idforn=fornecedor,
            idvende=vendedor,
            valorvend=valor_venda,
            descvend=0,
            totalvend=valor_venda,
            datavend='2023-07-19',  # Data atual
            valorcomissao=valor_venda * vendedor.porcvende / 100
        )

        # Cria um item de venda associado à venda
        ItensVenda.objects.create(
            idvend=venda,
            idprod=produto,
            valoritvend=produto.valorprod,
            qtditvend=quantidade,
            descitvend=0
        )

        # Atualiza a quantidade do produto
        novo_estoque = estoque_disponivel - quantidade
        if novo_estoque <= 0:
            produto.delete()
        else:
            produto.situprod = str(novo_estoque)
            produto.save()

        return redirect('home')  # Redireciona para a página inicial após concluir a venda

    # Se o método de requisição não for POST, exibe os dados dos clientes e produtos
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'trade/realizar_venda.html', {
        'clientes': clientes,
        'produtos': produtos,
    })
# Função para realizar o login do usuário
def login_view(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa o formulário de login
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():  # Se o formulário for válido, autentica o usuário
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Realiza o login do usuário
                return redirect('home')  # Redireciona para a página inicial
    else:
        form = AuthenticationForm()  # Se o método de requisição não for POST, exibe um formulário vazio
    return render(request, 'trade/login.html', {'form': form})

# Função para cadastrar um novo usuário
def cadastroUser(request):
    if request.method == 'POST':  # Se o método de requisição for POST, processa o formulário de cadastro
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # Se o formulário for válido, salva os dados do usuário
            user = form.save()
            username = user.username
            messages.success(request, 'Cadastro realizado com sucesso!')  # Exibe uma mensagem de sucesso
            return redirect('cadastroUser')  # Redireciona para a página de cadastro
    else:
        form = UserRegisterForm()  # Se o método de requisição não for POST, exibe um formulário vazio
    return render(request, 'trade/cadastroUser.html', {'form': form})
