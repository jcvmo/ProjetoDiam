from django.urls import include, path
from django.views.generic import TemplateView

from . import views # (. significa que importa views da mesma directoria)

app_name = 'principal'  # Defina o namespace aqui

urlpatterns = [
    path("receitas/", views.receitas, name='receitas'),
    path("receitas/minhas/", views.receitas_minhas, name='receitas_minhas'),
    path("receitas/<int:receita_id>", views.receitas_detalhe, name='receitas_detalhe'),
    path("receitas/criar", views.receitas_criar, name='receitas_criar'),
    path("receitas/<int:receita_id>/editar/", views.receitas_editar, name='receitas_editar'),
    path("receitas/<int:receita_id>/eliminar/", views.receitas_eliminar, name='receitas_eliminar'),
    path("ingredientes/", views.ingredientes, name='ingredientes'),
    path("ingredientes/<int:ingrediente_id>", views.ingredientes_detalhe, name='ingredientes_detalhe'),
    path("ingredientes/criar", views.ingredientes_criar, name='ingredientes_criar'),
    path("criar_user/", views.utilizador_criar_user, name='utilizador_criar_user'),
    path("criar_admin/", views.utilizador_criar_admin, name='utilizador_criar_admin'),
    path("login/", views.utilizador_login, name='utilizador_login'),
    path("logout/", views.utilizador_logout, name='utilizador_logout'),
    path("home/", views.home, name='home'),
    path("403/", TemplateView.as_view(template_name='403'))

]