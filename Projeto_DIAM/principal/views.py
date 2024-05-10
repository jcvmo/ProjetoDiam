from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Receita, User, Categoria, Ingrediente, ReceitaIngrediente, Utilizador


def check_admin(user):
    try:
        return user.utilizador.acesso == 2
    except Utilizador.DoesNotExist:
        return False

def home(request):
    user_count = User.objects.count()
    receitas_count = Receita.objects.count()
    ingredientes_count = Ingrediente.objects.count()
    return render(request, 'views/utilizador/home.html', {'user_count': user_count,'receitas_count': receitas_count,'ingredientes_count': ingredientes_count})

#receitas
def receitas(request):
    query = request.GET.get('query', '')
    ingredientes = request.GET.getlist('ingredients')  # Get list of selected ingredient ids

    if query:
        lista_receitas = Receita.objects.filter(
            receita_nome__icontains=query)  # Filter recipes by name containing the query
    else:
        lista_receitas = Receita.objects.all()

    if ingredientes:
        lista_receitas = lista_receitas.filter(receitaingrediente__ingrediente__ingrediente_id__in=ingredientes).distinct()

    lista_ingredientes = Ingrediente.objects.all()  # Fetch all ingredients for the dropdown

    return render(request, 'views/receitas/receitas_index.html', {
        'lista_receitas': lista_receitas,
        'query': query,
        'tipo': 1,
        'lista_ingredientes' : lista_ingredientes
    })

@login_required()
def receitas_minhas(request):
    lista_receitas = Receita.objects.filter(receita_user=request.user)
    return render(request, 'views/receitas/receitas_index.html', {'lista_receitas': lista_receitas ,'tipo' : 2 })



def receitas_detalhe(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_ingredientes = ReceitaIngrediente.objects.filter(receita=receita)
    return render(request, 'views/receitas/receitas_detalhe.html', {'receita': receita, 'receita_ingredientes':receita_ingredientes})

@login_required()
def receitas_editar(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_ingredientes = ReceitaIngrediente.objects.filter(receita=receita)

    if request.method == 'POST':
        receita.receita_nome = request.POST['receita_nome']
        receita.receita_descricao = request.POST['receita_descricao']
        receita.receita_tempo_confecao = request.POST['receita_tempo_confecao']

        if 'receita_imagem' in request.FILES:
            receita.receita_imagem = request.FILES['receita_imagem']
        receita.save()

        for ingrediente in receita_ingredientes:
            quantidade = f'ingrediente_{ingrediente.ingrediente.ingrediente_id}_quantidade'
            if quantidade in request.POST:
                ingrediente_quantidade = request.POST[quantidade]
                if ingrediente_quantidade.isdigit():
                    ingrediente.quantidade = int(ingrediente_quantidade)
                    ingrediente.save()

        return HttpResponseRedirect(reverse('principal:receitas_detalhe', args=(receita.receita_id,)))

    else:
        return render(request, 'views/receitas/receitas_editar.html', {
            'receita': receita,
            'receita_ingredientes': receita_ingredientes
        })

@login_required()
def receitas_criar(request):
    ingredientes = Ingrediente.objects.all()
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        user_chef = get_object_or_404(User, pk=request.user.id)

        receita_nome = request.POST['receita_nome']
        receita_descricao = request.POST['receita_descricao']
        receita_tempo_confecao = request.POST['receita_tempo_confecao']
        receita_user = user_chef


        nova_receita = Receita(receita_nome=receita_nome,
                               receita_descricao=receita_descricao,
                               receita_tempo_confecao=receita_tempo_confecao,
                               receita_user=receita_user)
        nova_receita.save()


        for ingrediente in ingredientes:
            quantidade = f'ingrediente_{ingrediente.ingrediente_id}_quantidade'
            ingrediente_quantidade = request.POST.get(quantidade, '0')


            if ingrediente_quantidade.isdigit() and int(ingrediente_quantidade) > 0:
                ReceitaIngrediente.objects.create(
                    receita=nova_receita,
                    ingrediente=ingrediente,
                    quantidade=int(ingrediente_quantidade)
                )
        if 'receita_imagem' in request.FILES:
            nova_receita.receita_imagem = request.FILES['receita_imagem']
            nova_receita.save()

        return HttpResponseRedirect(reverse('principal:receitas_detalhe', args=(nova_receita.receita_id,)))

    else:
        return render(request, 'views/receitas/receitas_criar.html', {'categorias': categorias})

def receitas_eliminar(request, receita_id):
    if request.method == 'POST':
        receita = get_object_or_404(Receita, pk=receita_id)
        receita.delete()
        return redirect('principal:receitas')
    else:
        return redirect('principal:receitas_detalhe', receita_id=receita_id)



#ingredientes

@login_required()
@user_passes_test(check_admin)
def ingredientes(request):
    lista_ingredientes = Ingrediente.objects.all()
    return render(request, 'views/ingredientes/ingredientes_index.html', {'lista_ingredientes': lista_ingredientes})

@login_required()
@user_passes_test(check_admin)

def ingredientes_detalhe(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, pk=ingrediente_id)
    return render(request, 'views/ingredientes/ingredientes_detalhe.html', {'ingrediente': ingrediente})

@login_required()
@user_passes_test(check_admin)

def ingredientes_criar(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        user_admin = User.objects.get(pk=1)

        ingrediente_nome = request.POST['ingrediente_nome']
        ingrediente_categoria = Categoria.objects.get(pk=request.POST.get('categoria_id'))
        ingrediente_user = user_admin


        novo_ingrediente = Ingrediente(ingrediente_nome=ingrediente_nome,
                               ingrediente_categoria=ingrediente_categoria,
                               ingrediente_user=ingrediente_user)
        novo_ingrediente.save()


        if 'ingrediente_imagem' in request.FILES:
            novo_ingrediente.ingrediente_imagem = request.FILES['ingrediente_imagem']
            novo_ingrediente.save()

        return HttpResponseRedirect(reverse('principal:ingredientes_detalhe', args=(novo_ingrediente.ingrediente_id,)))

    else:
        return render(request, 'views/ingredientes/ingredientes_criar.html', {'categorias': categorias})


#armário
def armário(request):
    user_chef = User.objects.get(pk=1)
    receita = get_object_or_404(Receita, user_chef=user_chef)
    return render(request, 'views/receitas/receitas_detalhe.html', {'receita': receita})

#utilizador

def utilizador_criar_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        telefone = request.POST['telefone']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'An account with this username already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')

        novo_user = User.objects.create_user(username,
                                              email,
                                              password,
                                              )

        novo_utilizador =Utilizador(user=novo_user, telefone=telefone, ativo=True, acesso=1)


        novo_utilizador.save()

        auth_login(request, novo_user)

        return render(request,'views/utilizador/home.html')

    return render(request, 'views/utilizador/utilizador_criar.html')

@login_required()
@user_passes_test(check_admin)
def utilizador_criar_admin(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        telefone = request.POST['telefone']
        password = request.POST['password']
        acesso = 2
        criador = User.objects.get(pk=1)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'An account with this username already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')

        novo_user = User.objects.create_user(username,
                                             email,
                                             password,
                                             )

        novo_utilizador = Utilizador(user=novo_user, telefone=telefone, ativo=True, acesso=2)

        novo_utilizador.save()

        auth_login(request, novo_user)

        #return HttpResponseRedirect(reverse('principal:admin_dashboard'))
        return HttpResponseRedirect(reverse('principal:home'))

    return render(request, 'views/utilizador/utilizador_criar.html')


def utilizador_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #  if novo_utilizador.user_password == user_password:
        novo_utilizador = authenticate(username=username, password=password)

        if novo_utilizador is not None:
            login(request, novo_utilizador)
            return redirect('principal:home')
        else:
            messages.error(request, 'Username ou Password inválidos')
            return render(request, 'views/utilizador/login.html')

    return render(request, 'views/utilizador/login.html')


@login_required()
def utilizador_logout(request):
    if request.method == 'POST':
        request.session.flush()
        return HttpResponseRedirect(reverse('principal:home'))

    return render(request, 'views/utilizador/logout.html')
