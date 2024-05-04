from principal.models import Receita


def listar_questoes():
    receitas = Receita.objects.all()
    if receitas:
        print("Lista de Receitas:")
        for receita in receitas:
            print(receita.receita_nome)
    else:
        print("Não há questões no banco de dados.")
