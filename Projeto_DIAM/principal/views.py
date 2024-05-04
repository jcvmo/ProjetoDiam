from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Receita, User, Categoria, Ingrediente

#receitas
def receitas(request):
    lista_receitas = Receita.objects.all()
    return render(request, 'views/receitas/receitas_index.html', {'lista_receitas': lista_receitas})
def receitas_detalhe(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    return render(request, 'views/receitas/receitas_detalhe.html', {'receita': receita})
def receitas_criar(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        user_chef = User.objects.get(pk=1)

        receita_nome = request.POST['receita_nome']
        receita_descricao = request.POST['receita_descricao']
        receita_tempo_confecao = request.POST['receita_tempo_confecao']
        receita_user = user_chef


        nova_receita = Receita(receita_nome=receita_nome,
                               receita_descricao=receita_descricao,
                               receita_tempo_confecao=receita_tempo_confecao,
                               receita_user=receita_user)
        nova_receita.save()

        for ingrediente_id in request.POST.getlist('ingredientes'):
            nova_receita.ingredientes.add(Ingrediente.objects.get(pk=ingrediente_id))

        nova_receita.save()

        if 'receita_imagem' in request.FILES:
            nova_receita.receita_imagem = request.FILES['receita_imagem']
            nova_receita.save()

        return HttpResponseRedirect(reverse('principal:receitas_detalhe', args=(nova_receita.receita_id,)))

    else:
        return render(request, 'views/receitas/receitas_criar.html', {'categorias': categorias})



#ingredientes
def ingredientes(request):
    lista_ingredientes = Ingrediente.objects.all()
    return render(request, 'views/ingredientes/ingredientes_index.html', {'lista_ingredientes': lista_ingredientes})
def ingredientes_detalhe(request, ingrediente_id):
    ingrediente = get_object_or_404(Ingrediente, pk=ingrediente_id)
    return render(request, 'views/ingredientes/ingredientes_detalhe.html', {'ingrediente': ingrediente})
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
        user_nome_utilizador = request.POST['user_nome_utilizador']
        user_email = request.POST['user_email']
        user_telefone = request.POST['user_telefone']
        user_password = request.POST['user_password']
        user_acesso = 1

        if User.objects.filter(user_nome_utilizador=user_nome_utilizador).exists():
            messages.error(request, 'An account with this username already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')
        if User.objects.filter(user_email=user_email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')


        novo_utilizador = User(user_nome_utilizador=user_nome_utilizador,
                                     user_email=user_email,
                                     user_telefone = user_telefone,
                                     user_password = user_password,
                                     user_ativo = True,
                                     user_acesso = user_acesso,
                               )
        novo_utilizador.save()

        return HttpResponseRedirect(reverse('principal:receitas'))

    return render(request, 'views/utilizador/utilizador_criar.html')


def utilizador_criar_admin(request):

    if request.method == 'POST':
        user_nome_utilizador = request.POST['user_nome_utilizador']
        user_email = request.POST['user_email']
        user_telefone = request.POST['user_telefone']
        user_password = request.POST['user_password']
        user_acesso = 2
        user_criador = User.objects.get(pk=1)

        if User.objects.filter(user_nome_utilizador=user_nome_utilizador).exists():
            messages.error(request, 'An account with this username already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')
        if User.objects.filter(user_email=user_email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'views/utilizador/utilizador_criar.html')

        novo_utilizador = User(user_nome_utilizador=user_nome_utilizador,
                                     user_email= user_email,
                                     user_telefone = user_telefone,
                                     user_password = user_password,
                                     user_ativo = True,
                                     user_acesso = user_acesso,
                                     user_criador = user_criador,
                               )
        novo_utilizador.save()

        request.session['user_id'] = novo_utilizador.user_id

        #return HttpResponseRedirect(reverse('principal:admin_dashboard'))
        return HttpResponseRedirect(reverse('principal:receitas'))

    return render(request, 'views/utilizador/utilizador_criar.html')


def utilizador_login(request):
    if request.method == 'POST':
        user_nome_utilizador = request.POST['user_nome_utilizador']
        user_password = request.POST['user_password']

        if User.objects.filter(user_nome_utilizador=user_nome_utilizador).exists():
            novo_utilizador = User.objects.get(user_nome_utilizador=user_nome_utilizador)

            if novo_utilizador.user_password == user_password:
                request.session['user_id'] = novo_utilizador.user_id
                return HttpResponseRedirect(reverse('principal:receitas'))
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'Invalid user.')
        return render(request, 'views/utilizador/login.html')

    return render(request, 'views/utilizador/login.html')


