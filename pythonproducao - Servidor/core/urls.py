from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
# ADICIONE 'excluir_foto_rcp' NA LISTA DE IMPORTAÇÃO ABAIXO:
from producao.views import dashboard_producao, lista_logs, nova_rcp, editar_rcp, excluir_foto_rcp, gerenciar_fotos_modal, upload_foto_modal, servir_foto_servidor
from producao import views
from django.conf import settings
from django.conf.urls.static import static 
from producao import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', dashboard_producao, name='dashboard'),
    path('novo/', nova_rcp, name='nova_rcp'),
    path('editar/<int:rcp_id>/', editar_rcp, name='editar_rcp'),
    path('logs/', lista_logs, name='lista_logs'),
    path('foto/excluir/<int:foto_id>/', excluir_foto_rcp, name='excluir_foto'),
    path('notificacao/lida/<int:id>/', views.marcar_notificacao_lida, name='marcar_lida'),
    path('notificacoes/checar/', views.carregar_notificacoes, name='carregar_notificacoes'),
    path('rcp/certificado/excluir/<int:cert_id>/', views.excluir_certificado, name='excluir_certificado'),
    path('excluir-fotos-massa/', views.excluir_fotos_massa, name='excluir_fotos_massa'),
    path('rcp/fotos/modal/<int:rcp_id>/', views.gerenciar_fotos_modal, name='fotos_modal'), 
    #path('rcp/fotos/upload/<int:rcp_id>/', views.upload_foto_modal, name='upload_foto_modal'),
    path('rcp/foto/excluir/<int:foto_id>/', views.excluir_foto_simples, name='excluir_foto_simples'),
    path('gerar-excel/<int:rcp_id>/', views.gerar_excel_rcp, name='gerar_excel_rcp'),
    path('rcp/pasta/<str:cliente_nome>/', views.abrir_pasta_cliente, name='url_abrir_pasta'),
    path('rcp/visualizar/<str:cliente_nome>/<str:rcp_numero>/', views.visualizar_arquivo_rcp, name='url_visualizar_rcp'),
    path('rcp/salvar-campo/', views.salvar_campo_rcp, name='salvar_campo_rcp'),
    path('rcp/dados-atuais/<int:rcp_id>/', views.rcp_dados_atuais, name='rcp_dados_atuais'),
    path('rcp/foto/ver/<int:foto_id>/', views.servir_foto_servidor, name='servir_foto_rede'),
    path('chat/obter-id-privado/<int:user_id>/', views.obter_id_chat_privado, name='obter_id_chat_privado'),
    path('chat/historico/<int:grupo_id>/', views.buscar_historico_chat, name='buscar_historico_chat'),
    
    # Garante que a rota de upload aponte para a função que salvamos na rede
    path('rcp/fotos/upload/<int:rcp_id>/', views.upload_foto_modal, name='upload_foto_modal'),
   # Tela principal do Dashboard de Perdas
    path('producao/perdas/', views.dashboard_perdas, name='dashboard_perdas'),
    
    # Endpoint AJAX para salvar o registro de peça matada
    path('producao/perdas/salvar/', views.salvar_perda_ajax, name='salvar_perda_ajax'),
    
    # Endpoint AJAX que alimenta o Chart.js com os dados do gráfico
    path('producao/perdas/dados-grafico/', views.dados_grafico_ajax, name='dados_grafico_ajax'),
    
    # URL para adicionar funcionário via AJAX
    path('producao/perdas/funcionario/adicionar/', views.adicionar_funcionario_ajax, name='adicionar_funcionario_ajax'),

    # ADICIONE ESTA LINHA AQUI ABAIXO:
    path('producao/perdas/historico/<int:funcionario_id>/', views.historico_funcionario_ajax, name='historico_funcionario_ajax'),
    path('perdas/editar-motivo/', views.editar_motivo_ajax, name='editar_motivo_ajax'),
    path('editar-usuario/', views.editar_usuario_ajax, name='editar_usuario_ajax'),
    path('excluir-usuario/', views.excluir_usuario_ajax, name='excluir_usuario_ajax'),
    path('chat/fotos-matada/<int:id_registro>/', views.fotos_peca_matada_modal, name='fotos_peca_matada_modal'),
    path('servir-foto-peca/<int:foto_id>/', views.servir_foto_peca_matada, name='servir_foto_peca_matada'),
    path('perdas/modal-edicao/<int:perda_id>/', views.carregar_modal_edicao, name='modal_edicao_perda'),
    path('perdas/atualizar/<int:perda_id>/', views.atualizar_perda_ajax, name='atualizar_perda_ajax')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
