from django.urls import path
from . import views

urlpatterns = [
    path('livros/', views.listar_livros, name='listar_livros'),
    path('livros/novo/', views.livro_criar, name='livro_criar'),
    path('livros/<int:pk>/editar/', views.livro_editar, name='livro_editar'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
