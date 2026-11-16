import io
import mimetypes
import textwrap
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from .models import OrdemServico, RcpFoto, NotificacaoSetor, CertificadoRCP, QuadroObras, GrupoChat, Mensagem, FuncionarioProducao, RegistroPecaMatada, FotoPecaMatada
from .forms import RCPForm
from django.db.models import Q, CharField, Sum
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta
from openpyxl import load_workbook
import os
import subprocess
from fpdf import FPDF
import comtypes.client
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import json
from datetime import datetime, date
import shutil
# --- FUNÇÕES DE AUXÍLIO ---



def home(request):
    todos_usuarios = User.objects.exclude(id=request.user.id)
    
    # Lista para salvar os IDs de todos os chats privados ou grupos do usuário logado
    # (Útil se seu JavaScript precisar monitorar os canais do WebSocket)
    meus_grupo_ids = list(GrupoChat.objects.filter(membros=request.user).values_list('id', flat=True))
    
    total_nao_lidas_global = 0

    # 2. Vamos rodar cada usuário da lista para descobrir as mensagens não lidas no chat 1x1
    for u in todos_usuarios:
        # Busca o chat privado que seja específico entre você (request.user) e este contato (u)
        chat_privado = GrupoChat.objects.filter(
            e_grupo=False, 
            membros=request.user
        ).filter(membros=u).first()

        # Se esse chat já existir, contamos as mensagens não lidas dele
        if chat_privado:
            u.mensagens_nao_lidas = Mensagem.objects.filter(
                autor=u,        # Mensagem enviada pelo contato
                grupo=chat_privado, # Dentro do chat privado de vocês
                lida=False      # Que ainda não foi lida
            ).count()
        else:
            # Se eles nunca se falaram, o chat não existe e as não lidas são 0
            u.mensagens_nao_lidas = 0
        
        # Acumula para o contador geral (botão verde ou notificações globais)
        total_nao_lidas_global += u.mensagens_nao_lidas

    # 3. Montamos o contexto para o HTML
    context = {
        'todos_usuarios': todos_usuarios,
        'meus_grupo_ids': meus_grupo_ids, 
        'total_nao_lidas_global': total_nao_lidas_global,
        # ... mantenha aqui outros contextos que sua home já tinha ...
    }
    
    return render(request, 'home.html', context)


def buscar_historico_chat(request, grupo_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado'}, status=401)
    
    grupo = get_object_or_404(GrupoChat, id=grupo_id)
    
    if request.user not in grupo.membros.all():
        return JsonResponse({'error': 'Acesso negado'}, status=403)

    mensagens = Mensagem.objects.filter(grupo=grupo).order_by('data_envio')
    
    dados = []
    for m in mensagens:
        dados.append({
            'id': m.id,             # ESSENCIAL
            'usuario': m.autor.username,
            'mensagem': m.texto,         
            'data': m.data_envio.strftime('%H:%M'),
            'lida': m.lida          # ESSENCIAL para o check azul persistir
        })
    
    return JsonResponse({'historico': dados})


def quadro_obras(request):
    obras = QuadroObras.objects.all().order_by('-data_inicio_obra')
    return render(request, 'producao/quadro_obras.html', {'obras': obras})

def e_da_qualidade(user):
    """Verifica se o usuário pertence ao grupo Qualidade ou é Superuser."""
    return user.groups.filter(name='Qualidade').exists() or user.is_superuser

# --- marca como lida a notificação para nao aparecer mais ---
@csrf_exempt # Adicione isso para o HTMX conseguir postar sem erro de segurança
@login_required
def marcar_notificacao_lida(request, id):
    notificacao = get_object_or_404(NotificacaoSetor, id=id)
    
    # Em vez de notificacao.lida = True, fazemos:
    notificacao.usuarios_que_leram.add(request.user)
    
    if request.headers.get('HX-Request'):
        return HttpResponse("") 
        
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
# --- VIEWS PRINCIPAIS ---

@login_required
def dashboard_producao(request):
    # --- 1. LÓGICA DE ALERTAS POR SETOR ---
    user_setor = None
    
    # Pegamos os nomes dos grupos do usuário logado
    user_groups = request.user.groups.values_list('name', flat=True)

    # Corrigindo a lógica: Se o usuário é do grupo X, ele vê alertas destinados ao setor X
    if 'Comercial' in user_groups:
        user_setor = 'COMERCIAL'
    elif 'Qualidade' in user_groups:
        user_setor = 'QUALIDADE'
    elif 'Producao' in user_groups:
        user_setor = 'PRODUCAO'

    # Busca notificações não lidas para o setor identificado
    if user_setor:
        alertas = NotificacaoSetor.objects.filter(
            setor_destino=user_setor
        ).exclude(
            usuarios_que_leram=request.user
        )
    else:
        alertas = []

    'aqui'
    # --- 2. LÓGICA DE BUSCA E FILTRAGEM --- 
    query = request.GET.get('busca', '').strip()
    queryset = OrdemServico.objects.all().order_by('-rcp')

    if query:
        if query.isdigit():
            queryset = queryset.filter(Q(rcp=query) | Q(cliente__icontains=query))
        else:
            queryset = queryset.filter(Q(cliente__icontains=query) | Q(os__icontains=query))

    # --- 3. ORGANIZAÇÃO DO CONTEXTO ---
    context = {
        'alertas': alertas,
        'todas_rcps': queryset,
        
        # Filtros por Status otimizados (usam o queryset já filtrado pela busca)
        'aguardando': queryset.filter(status='AGUARDANDO LIBERAÇÃO'),
        'aguardando_count': queryset.filter(status='AGUARDANDO LIBERAÇÃO').count(),
        
        'aguardando_nota': queryset.filter(status='AGUARDANDO NOTA DE SAIDA'),
        'aguardando_nota_count': queryset.filter(status='AGUARDANDO NOTA DE SAIDA').count(),

        'liberado_producao': queryset.filter(status='LIBERADO PARA PRODUÇÃO'),
        'liberado_producao_count': queryset.filter(status='LIBERADO PARA PRODUÇÃO').count(),
        
        'liberado_inspecao': queryset.filter(status='AGUARDANDO INSPEÇÃO INICIAL'),
        'liberado_inspecao_count': queryset.filter(status='AGUARDANDO INSPEÇÃO INICIAL').count(),

        'em_producao': queryset.filter(status='EM PRODUÇÃO'),
        'producao_count': queryset.filter(status='EM PRODUÇÃO').count(),
        
        'inspecao_final': queryset.filter(status='AGUARDANDO INSPEÇÃO FINAL'),
        'inspecao_count': queryset.filter(status='AGUARDANDO INSPEÇÃO FINAL').count(),
        
        'aguardando_retirada': queryset.filter(status='AGUARDANDO RETIRADA'),
        'retirada_count': queryset.filter(status='AGUARDANDO RETIRADA').count(),
        
        'entregue_ao_cliente': queryset.filter(status='ENTREGUE AO CLIENTE'),
        'entregue_ao_cliente_count': queryset.filter(status='ENTREGUE AO CLIENTE').count(),
    }
    
    return render(request, 'producao/dashboard.html', context)


#CICLO DE GERAR RCP -> EXCEL -> PDF -> VISUALIZAR PDF
from django.http import JsonResponse
import aspose.cells as cells

def gerar_excel_rcp(request, rcp_id):
    """
    Gera o arquivo Excel da RCP preenchendo um modelo existente 
    e entrega o download diretamente via memória (BytesIO).
    """
    # 1. Busca os dados
    rcp = get_object_or_404(OrdemServico, pk=rcp_id)

    empresa_selecionada = request.GET.get('empresa', 'eletroinox')

    # 2. Define o nome do arquivo modelo baseado na escolha
    if empresa_selecionada == 'azzure':
        nome_modelo = 'modelo_rcp_azzure.xlsx'
    elif empresa_selecionada == 'ag':
        nome_modelo = 'modelo_rcp_ag.xlsx'
    else:
        nome_modelo = 'modelo_rcp.xlsx'

    # 2. Configuração de Caminhos (Garanta que a pasta e o modelo existam no servidor)
    caminho_modelo = os.path.join(settings.BASE_DIR, 'media', 'rcp', nome_modelo)

    if not os.path.exists(caminho_modelo):
        return HttpResponse(f"Erro: Modelo não encontrado no servidor.", status=404)

    try:
        # 3. Carregar o Excel
        wb = load_workbook(caminho_modelo)
        ws = wb.active

        # Formatação de Datas
        data_formatada = timezone.localtime(rcp.data_entrada_peca).strftime('%d/%m/%Y %H:%M')
        data_expedicao_formatada = timezone.localtime(rcp.data_expedicao).strftime('%d/%m/%Y %H:%M') if rcp.data_expedicao else ''

        # Preenchimento
        ws['V1'] = rcp.rcp
        if rcp.os != "0000/26":
            ws['U7'] = rcp.os
        ws['C7'] = rcp.cliente
        ws['S14'] = data_formatada
        ws['S16'] = rcp.nf_cliente
        ws['H30'] = rcp.proposta
        ws['U53'] = rcp.nf_saida
        ws['G53'] = data_expedicao_formatada
        ws['M55'] = rcp.placa_veiculo
        ws['A54'] = rcp.expedido_por
        ws['K23'] = rcp.tipo_servico
        
        import re
        texto = rcp.descricao_peca
        if not texto or str(texto).strip() == "":
            total_pecas = ""
        else:
            partes = re.split(r',|\s+-\s+|\s+e\s+', str(texto))
            
            total_pecas = 0
            
            for parte in partes:
                parte = parte.strip()
                
                # Procura por números logo no início do trecho
                match = re.match(r'^(\d+)', parte)
                
                if match:
                    total_pecas += int(match.group(1))
        
        ws['S15'] = total_pecas
        # Lógica de Descrição da Peça
        largura_da_linha = 60 
        celulas_destino = ['C8', 'C9', 'C10', 'C11', 'C12', 'C13']
        linha_atual_excel = 0

        if rcp.descricao_peca:
            paragrafos = rcp.descricao_peca.splitlines()
            for p in paragrafos:
                if linha_atual_excel >= len(celulas_destino): break
                if not p.strip():
                    linha_atual_excel += 1
                    continue
                sub_linhas = textwrap.wrap(p, width=largura_da_linha)
                for sl in sub_linhas:
                    if linha_atual_excel < len(celulas_destino):
                        ws[celulas_destino[linha_atual_excel]] = sl
                        linha_atual_excel += 1

        # 4. Salvar em Buffer de Memória
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        # Importante fechar o workbook para liberar memória
        wb.close()

        # 5. Preparar a Resposta
        nome_cliente = str(rcp.cliente).strip().replace("/", "-").replace("\\", "-")
        nome_arquivo = f"RCP_{rcp.rcp}_{nome_cliente[:20]}.xlsx"

        # Mudamos para HttpResponse para ter controle total dos headers
        response = HttpResponse(
            buffer.getvalue(), 
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
        
        # Isso ajuda a evitar o erro de "Unexpected Token P" no JavaScript
        response['Content-Length'] = len(buffer.getvalue())
        
        return response

    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
        return HttpResponse(f"Erro ao processar Excel: {e}", status=500)
    
def abrir_pasta_cliente(request, cliente_nome):
    import os
    # Localiza a pasta do cliente
    caminho_pasta = os.path.join(settings.MEDIA_ROOT, 'rcp', cliente_nome)
    
    arquivos_encontrados = []
    if os.path.exists(caminho_pasta):
        for f in os.listdir(caminho_pasta):
            if f.endswith(('.xlsx', '.pdf')):
                # Criamos um dicionário com o nome e a URL do arquivo
                url = f"{settings.MEDIA_URL}rcp/{cliente_nome}/{f}"
                arquivos_encontrados.append({'nome': f, 'url': url})

    return render(request, 'rcp/listar_arquivos.html', {
        'arquivos': arquivos_encontrados,
        'cliente': cliente_nome
    })


def visualizar_arquivo_rcp(request, cliente_nome, rcp_numero):
    # Usamos o strip() para garantir que não haja espaços sobrando
    cliente_limpo = str(cliente_nome).strip()
    
    # Nome exatamente como foi salvo na função de gerar
    nome_arquivo = f"RCP {rcp_numero} - {cliente_limpo[:20]}.pdf"
    
    # Caminho completo
    caminho_arquivo = os.path.join(settings.MEDIA_ROOT, 'rcp', cliente_limpo, nome_arquivo)

    if os.path.exists(caminho_arquivo):
        # O FileResponse precisa do import que adicionamos acima
        return FileResponse(open(caminho_arquivo, 'rb'), content_type='application/pdf')
    else:
        # Se entrar aqui, é porque o caminho gerado acima não bate com o arquivo na pasta
        return render(request, 'rcp/erro_arquivo.html', {
            'mensagem': f"O arquivo '{nome_arquivo}' não foi encontrado na pasta do cliente.",
            'cliente': cliente_limpo
        })

#view do chat
def obter_id_chat_privado(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autorizado'}, status=401)
    
    outro_usuario = get_object_or_404(User, id=user_id)
    # Chama o método que criamos no Model
    chat = GrupoChat.obter_ou_criar_privado(request.user, outro_usuario)
    
    return JsonResponse({'id': chat.id})



# --- VIEWS DE CRIAÇÃO, EDIÇÃO E EXCLUSÃO DE RCPs ---

@login_required
@user_passes_test(e_da_qualidade, login_url='dashboard')
def nova_rcp(request):
    """Cria uma nova RCP garantindo a numeração sequencial correta."""
    if request.method == 'POST':
        dados_post = request.POST.copy()
        
        # Se o version não estiver nos dados, injetamos o valor '1'
        if not dados_post.get('version'):
            dados_post['version'] = '1'
        
        form = RCPForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Gerar numeração sequencial
                    ultimo = OrdemServico.objects.select_for_update().order_by('rcp').last()
                    proximo = (ultimo.rcp + 1) if ultimo else 1
                    
                    obj = form.save(commit=False)
                    obj.rcp = proximo
                    
                        
                    obj.save()

                    # 2. Processar arquivos opcionais (Fotos e Certificados)
                    for f in request.FILES.getlist('fotos_antes'):
                        RcpFoto.objects.create(rcp=obj, imagem=f, tipo='antes')
                    
                    for f in request.FILES.getlist('fotos_apos'):
                        RcpFoto.objects.create(rcp=obj, imagem=f, tipo='apos')

                    for f in request.FILES.getlist('certificados_novos'):
                        CertificadoRCP.objects.create(rcp=obj, arquivo=f, nome_exibicao=f.name)

                    messages.success(request, f"RCP {obj.rcp} criada com sucesso!")
                    return redirect('dashboard')
            except Exception as e:
                print(f"Erro ao salvar RCP: {e}")
                messages.error(request, f"Erro interno ao salvar: {e}")
        else:
            # Caso o formulário tenha erros de validação
            print("Erros do Formulário:", form.errors)
            messages.error(request, "Erro no formulário. Verifique os campos obrigatórios.")
    
    else:
        # Este ELSE é executado quando o método é GET (ao abrir a página)
        ultimo_registro = OrdemServico.objects.order_by('rcp').last()
        proximo_numero = (ultimo_registro.rcp + 1) if ultimo_registro else 1
        form = RCPForm(initial={'rcp': proximo_numero}, user=request.user)
    
    # O return final deve estar fora de todos os blocos IF/ELSE de método
    return render(request, 'producao/form_rcp.html', {'form': form, 'titulo': 'Nova RCP'})

@login_required
def editar_rcp(request, rcp_id):
    ordem = get_object_or_404(OrdemServico, rcp=rcp_id)
    
    if request.method == 'POST':
        # Mantemos o formulário para processar os arquivos (fotos/pdfs)
        form = RCPForm(request.POST, request.FILES, instance=ordem, user=request.user)
        
        if form.is_valid():
            try:
                # 1. Salvamos os arquivos e M2M primeiro
                obj = form.save(commit=False)
                
                # IMPORTANTE: No clique do botão "Salvar", limpamos o bloqueio de edição
                obj.editando_por = None
                obj.editando_desde = None
                
                # Aqui salvamos o objeto. Como os textos já foram salvos via AJAX, 
                # esse save servirá para garantir o Status e os arquivos.
                obj.save() 
                form.save_m2m()

             # --- AQUI ESTÁ O AJUSTE PARA FOTOS ANTES ---
                for f in request.FILES.getlist('fotos_antes'):
                    try:
                        # Usa a função de rede em vez do salvamento padrão
                        caminho_rede = salvar_foto_rede(f, obj, 'Antes')
                        RcpFoto.objects.create(rcp=obj, imagem=caminho_rede, tipo='antes')
                    except Exception as e:
                        messages.error(request, f"Erro ao salvar foto 'Antes' na rede: {e}")

                # --- AQUI ESTÁ O AJUSTE PARA FOTOS APÓS ---
                for f in request.FILES.getlist('fotos_apos'):
                    try:
                        caminho_rede = salvar_foto_rede(f, obj, 'Apos')
                        RcpFoto.objects.create(rcp=obj, imagem=caminho_rede, tipo='apos')
                    except Exception as e:
                        messages.error(request, f"Erro ao salvar foto 'Após' na rede: {e}")
                        
                # 3. Processamento de novos Certificados (Seu código original)
                arquivos_pdfs = request.FILES.getlist('certificados_novos')
                for f in arquivos_pdfs:
                    CertificadoRCP.objects.create(rcp=obj, arquivo=f, nome_exibicao=f.name)

                messages.success(request, "Processamento de arquivos concluído!")
                return redirect('editar_rcp', rcp_id=rcp_id)

            except Exception as e:
                messages.error(request, f"Erro ao processar: {e}")
    else:
        # GET: Marca presença de quem está editando
        ordem.editando_por = request.user
        ordem.editando_desde = timezone.now()
        ordem.save(update_fields=['editando_por', 'editando_desde'])
        form = RCPForm(instance=ordem, user=request.user)

    return render(request, 'producao/form_rcp.html', {'form': form, 'rcp': ordem})

@require_POST
@login_required
def salvar_campo_rcp(request):
    rcp_id = request.POST.get('rcp_id')
    if not rcp_id or rcp_id == '':
        return JsonResponse({
            'status': 'ignorado', 
            'message': 'Campo não salvo: RCP ainda não possui ID (Nova RCP).'
        }, status=200) # Retornamos 200 para não gerar erro no console

    # Se chegou aqui, o ID existe, então fazemos o get_object_or_404
    ordem = get_object_or_404(OrdemServico, rcp=rcp_id)
    nome_campo = request.POST.get('campo')
    novo_valor = request.POST.get('valor')
    
    ordem = get_object_or_404(OrdemServico, rcp=rcp_id)
    
    # Verifica se o campo existe no modelo para evitar erros de sistema
    campos_permitidos = [f.name for f in OrdemServico._meta.get_fields()]
    
    if nome_campo in campos_permitidos:
        try:
            # Se o valor vier vazio do JS, salvamos como None no banco
            valor_final = novo_valor if novo_valor.strip() != "" else None
            setattr(ordem, nome_campo, valor_final)
            ordem._history_user = request.user
            # Salva APENAS a coluna que foi modificada
            ordem.save(update_fields=[nome_campo])
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'erro', 'message': 'Campo inválido'}, status=400)

@login_required
def rcp_dados_atuais(request, rcp_id):
    ordem = get_object_or_404(OrdemServico, rcp=rcp_id)
    
    # Função auxiliar para formatar datas apenas se elas existirem
    def fmt_data(dt):
        if dt:
            # Converte para o fuso horário local e formata
            return timezone.localtime(dt).strftime('%Y-%m-%dT%H:%M')
        return ""

    dados = {
        # COMERCIAL
        'os': ordem.os or "",
        'cliente': ordem.cliente or "",
        'proposta': ordem.proposta or "",
        'nf_saida': ordem.nf_saida or "",
        'tipo_servico': ordem.tipo_servico or "",
        'prioridade': ordem.prioridade or "",
        'data_liberacao': fmt_data(ordem.data_liberacao),
        'liberado_por': ordem.liberado_por or "",
        'observacao_comercial': ordem.observacao_comercial or "",

        # QUALIDADE
        'rcp': ordem.rcp,
        'nf_cliente': ordem.nf_cliente or "",
        'data_entrada_peca': fmt_data(ordem.data_entrada_peca),
        'descricao_peca': ordem.descricao_peca or "",
        'obs_qualidade': ordem.obs_qualidade or "",
        'previsao_entrega_qualidade': fmt_data(ordem.previsao_entrega_qualidade),
        'data_inspecao_inicial': fmt_data(ordem.data_inspecao_inicial),

        # EXPEDIÇÃO
        'nome_motorista': ordem.nome_motorista or "",
        'placa_veiculo': ordem.placa_veiculo or "",
        'obs_expedicao': ordem.obs_expedicao or "",
        'data_expedicao': fmt_data(ordem.data_expedicao),
        'expedido_por': ordem.expedido_por or "",

        # PRODUÇÃO
        'status': ordem.status or "",
        'inicio_producao': fmt_data(ordem.inicio_producao),
        'operador': ordem.operador or "",
        'previsao_conclusao_prod': fmt_data(ordem.previsao_conclusao_prod),
        'data_finaliza_producao': fmt_data(ordem.data_finaliza_producao),
        'obs_producao': ordem.obs_producao or "",
        'data_inspecao_final': fmt_data(ordem.data_inspecao_final),
    }
    
    return JsonResponse(dados)
   
def salvar_foto_rede(arquivo, rcp_obj, tipo):
    """
    Salva a foto organizando em: Cliente > RCP XXX > ANTES ou APOS
    """
    # 1. Caminho base bruto
    caminho_base = r"\\Servinox\eletroinox\Recebimento e Expedição\FOTOS clientes"
    
    # 2. Limpeza de strings para evitar erros de diretório
    cliente_limpo = str(rcp_obj.cliente).strip().replace("/", "-").replace("\\", "-")
    
    # --- NOVA LÓGICA DE PASTAS ---
    # Pasta Principal: "Cliente RCP 1234"
    nome_pasta_rcp = f"{cliente_limpo} RCP {rcp_obj.rcp}"
    
    # Subpasta: "ANTES" ou "APOS" (baseado no parâmetro 'tipo')
    subpasta_tipo = tipo.upper().strip() 
    
    # 3. Construção do diretório com a nova hierarquia
    # O join vai criar: ...\Cliente\Cliente RCP 1234\ANTES (ou APOS)
    diretorio_final = os.path.join(caminho_base, cliente_limpo, nome_pasta_rcp, subpasta_tipo)
    
    try:
        # O makedirs com exist_ok=True criará toda a árvore de pastas se não existir
        os.makedirs(diretorio_final, exist_ok=True)
        
        # 4. Define o nome do arquivo e o caminho completo
        caminho_arquivo = os.path.join(diretorio_final, arquivo.name)
        caminho_final = os.path.normpath(caminho_arquivo)
        
        # 5. Gravação física
        with open(caminho_final, 'wb+') as destination:
            for chunk in arquivo.chunks():
                destination.write(chunk)
        
        return caminho_final
        
    except Exception as e:
        print(f"Erro ao salvar foto na rede: {e}")
        raise e

def servir_foto_servidor(request, foto_id):
    foto = get_object_or_404(RcpFoto, id=foto_id)
    # 1. Caminho que está gravado no Banco de Dados
    caminho_banco = os.path.normpath(str(foto.imagem))
    
    # 2. Definição do Caminho Antigo (Ajuste para o caminho real da sua pasta única antiga)
    # Exemplo: se antes ficava tudo dentro de uma pasta chamada "Geral"
    caminho_base_antigo = r"D:\ELETROINOX\Sistemas\Controle_de_Producao\media\fotos_rcp"
    #C:\Users\Financeiro\Documents\pyjango\media\fotos_rcp
    #D:\ELETROINOX\Sistemas\Controle_de_Producao\media\fotos_rcp
    caminho_final = caminho_banco
 
    # Ajuste do prefixo de rede \\
    if not caminho_final.startswith('\\\\') and caminho_final.startswith('\\'):
        caminho_final = '\\\\' + caminho_final.lstrip('\\')

    # --- LÓGICA DE COMPATIBILIDADE ---
    # Se o arquivo não existe no caminho do banco, tentamos na pasta antiga
    if not os.path.exists(caminho_final):
        # Pega apenas o nome do arquivo (ex: foto123.jpg) ignorando as pastas
        nome_arquivo = os.path.basename(caminho_final)
        tentativa_caminho_antigo = os.path.join(caminho_base_antigo, nome_arquivo)
        
        if os.path.exists(tentativa_caminho_antigo):
            caminho_final = tentativa_caminho_antigo
        else:
            # Se não achou em nenhum dos dois, retorna erro 404
            return HttpResponse(f"ARQUIVO NÃO ENCONTRADO (Banco ou Pasta Antiga): {nome_arquivo}", status=404)
    # ---------------------------------

    try:
        img_file = open(caminho_final, 'rb')
        content_type, _ = mimetypes.guess_type(caminho_final)
        return FileResponse(img_file, content_type=content_type or 'image/jpeg')
    except PermissionError:
        return HttpResponse(f"PERMISSÃO NEGADA NA REDE: {caminho_final}", status=403)
    except Exception as e:
        return HttpResponse(f"ERRO AO ABRIR: {str(e)}", status=500)

    
@login_required
def excluir_fotos_massa(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            fotos = RcpFoto.objects.filter(id__in=ids)
            
            for foto in fotos:
                # Tenta apagar o arquivo físico no servidor de rede antes de apagar do banco
                if foto.imagem and os.path.exists(str(foto.imagem)):
                    try:
                        os.remove(str(foto.imagem))
                    except:
                        pass # Se não conseguir apagar o arquivo, segue para apagar o registro
            
            total = fotos.count()
            fotos.delete()
            return JsonResponse({'status': 'ok', 'apagados': total})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método inválido'}, status=405)

@login_required
def excluir_certificado(request, cert_id):
    # Busca o certificado ou retorna 404
    certificado = get_object_or_404(CertificadoRCP, id=cert_id)
    rcp_id = certificado.rcp.rcp  # Guarda o número da RCP para voltar para a tela de edição
    
    if request.method == 'POST' or True: # Aceita exclusão rápida via link se desejar
        # Apaga o arquivo físico da pasta media
        if certificado.arquivo:
            certificado.arquivo.delete()
        
        # Apaga o registro no banco de dados
        certificado.delete()
        
        messages.success(request, "Certificado excluído com sucesso!")
    
    return redirect('editar_rcp', rcp_id=rcp_id)

from django.core.paginator import Paginator
from django.db.models import Q
@login_required
def lista_logs(request):
    # Detecta qual aba o usuário está visualizando (padrão é 'os')
    tipo = request.GET.get('tipo', 'os')
    
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # ==========================================
    # FLUXO 1: HISTÓRICO DO CHAT
    # ==========================================
    if tipo == 'chat':
        historico_query = Mensagem.history.all().order_by('-history_date')

        usuario_filtro = request.GET.get('usuario')
        if usuario_filtro:
            historico_query = historico_query.filter(autor__username__icontains=usuario_filtro)

        if data_inicio and data_fim:
            historico_query = historico_query.filter(history_date__date__range=[data_inicio, data_fim])

        paginator = Paginator(historico_query, 10)
        page_number = request.GET.get('page')
        historico_paginado = paginator.get_page(page_number)

        campos_ignorar = ['id', 'data_edicao', 'data_envio', 'editada', 'grupo_id']

        for h in historico_paginado:
            h.mudancas = []
            if h.history_type == '+': h.acao_formatada = "Mensagem Enviada"
            elif h.history_type == '~': h.acao_formatada = "Mensagem Editada"
            elif h.history_type == '-': h.acao_formatada = "Mensagem Excluída"

            prev = h.prev_record
            if prev:
                delta = h.diff_against(prev)
                for change in delta.changes:
                    if change.field not in campos_ignorar:
                        h.mudancas.append({
                            'campo': change.field.replace('_', ' ').title(),
                            'antigo': change.old if change.old not in [None, '', 'None'] else "Vazio",
                            'novo': change.new if change.new not in [None, '', 'None'] else "Vazio"
                        })

    # ==========================================
    # FLUXO 2: HISTÓRICO DA ORDEM DE SERVIÇO 
    # ==========================================
    else:
        historico_query = OrdemServico.history.all().order_by('-history_date')

        rcp_filtro = request.GET.get('rcp')
        if rcp_filtro:
            historico_query = historico_query.filter(rcp=rcp_filtro)

        if data_inicio and data_fim:
            historico_query = historico_query.filter(history_date__date__range=[data_inicio, data_fim])

        paginator = Paginator(historico_query, 10)
        page_number = request.GET.get('page')
        historico_paginado = paginator.get_page(page_number)

        campos_ignorar = ['editando_desde', 'editando_por', 'id', 'ultima_alteracao', 'version']

        for h in historico_paginado:
            h.mudancas = []
            prev = h.prev_record
            if prev:
                delta = h.diff_against(prev)
                for change in delta.changes:
                    if change.field not in campos_ignorar:
                        h.mudancas.append({
                            'campo': change.field.replace('_', ' ').title(),
                            'antigo': change.old if change.old not in [None, '', 'None'] else "Vazio",
                            'novo': change.new if change.new not in [None, '', 'None'] else "Vazio"
                        })

    # Retorna para o mesmo template antigo, enviando a variável 'tipo' junto
    return render(request, 'logs.html', {
        'historico': historico_paginado, 
        'tipo': tipo
    })

@login_required
def excluir_foto_rcp(request, foto_id):
    foto = get_object_or_404(RcpFoto, id=foto_id)
    # Apagar arquivo físico
    if foto.imagem and os.path.exists(str(foto.imagem)):
        try:
            os.remove(str(foto.imagem))
        except:
            pass
    foto.delete() 
    messages.success(request, "Foto removida com sucesso.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def excluir_foto_simples(request, foto_id):
    foto = get_object_or_404(RcpFoto, id=foto_id)
    rcp_id = foto.rcp.rcp
    if foto.imagem and os.path.exists(str(foto.imagem)):
        try:
            os.remove(str(foto.imagem))
        except:
            pass
    foto.delete()
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}?abrir_modal={rcp_id}")

@login_required
def carregar_notificacoes(request):
    # 1. Filtro de tempo: Apenas notificações das ultimas 24 horas
   # 1. Filtro de tempo: Últimas 24 horas
    limite_data = timezone.now() - timedelta(days=1)

    # 2. Identificar Setor
    user_groups = request.user.groups.values_list('name', flat=True)
    user_setor = None
    
    if 'Comercial' in user_groups:
        user_setor = 'COMERCIAL'
    elif 'Qualidade' in user_groups:
        user_setor = 'QUALIDADE'
    elif 'Producao' in user_groups:
        user_setor = 'PRODUCAO'
    elif request.user.is_superuser:
        user_setor = 'ADMIN'

    # 3. Consulta Base (Não lidas e nas últimas 24h)
    alertas_query = NotificacaoSetor.objects.filter(
        data_criacao__gte=limite_data
    ).exclude(
        usuarios_que_leram=request.user
    )

    # Aplica filtro de setor
    if user_setor and user_setor != 'ADMIN':
        alertas_query = alertas_query.filter(setor_destino=user_setor)

    # 4. CONTAGEM REAL (Para o Sininho)
    # Fazemos o count antes de fatiar com [:10]
    total_alertas = alertas_query.count()

    # 5. LISTA PARA O MENU (Apenas as 10 mais recentes)
    alertas_lista = alertas_query.order_by('-data_criacao')[:10]

    return render(request, 'producao/notificacoes_list.html', {
        'alertas': alertas_lista,
        'total_alertas': total_alertas # Use isso no seu badge do HTML
    })


@login_required
def gerenciar_fotos_modal(request, rcp_id):
    rcp = get_object_or_404(OrdemServico, rcp=rcp_id)
    fotos = rcp.fotos.all()
    return render(request, 'producao/gerenciar_fotos.html', {'rcp': rcp, 'fotos': fotos})


def upload_foto_modal(request, rcp_id):
    
    if request.method == 'POST':
        rcp_obj = get_object_or_404(OrdemServico, rcp=rcp_id)
        arquivos = request.FILES.getlist('imagem')
        tipo_foto = request.POST.get('tipo', 'Antes')

        for f in arquivos:
            try:
                # Chama a função de salvamento na rede
                caminho_no_servidor = salvar_foto_rede(f, rcp_obj, tipo_foto)
                
                # Salva no banco o caminho da string
                RcpFoto.objects.create(
                    rcp=rcp_obj,
                    imagem=caminho_no_servidor,
                    tipo=tipo_foto.lower()
                )
            except Exception as e:
                messages.error(request, f"Erro ao salvar foto no servidor: {e}")
        
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}?abrir_modal={rcp_id}")
    return redirect('dashboard')



#peças matadas funções
@login_required
def dashboard_perdas(request):
    funcionarios = FuncionarioProducao.objects.filter(ativo=True).order_by('nome')
    return render(request, 'producao/dashboard_perdas.html', {'funcionarios': funcionarios})

@login_required
@require_POST
@login_required
@require_POST
def salvar_perda_ajax(request):
    funcionario_id = request.POST.get('funcionario_id')
    quantidade = request.POST.get('quantidade')
    motivo = request.POST.get('motivo', '')
    os_id = request.POST.get('os_id')
    data_texto = request.POST.get('data_ocorrencia') # Ex: "2026-05-26T14:30"

    if not funcionario_id or not quantidade or not data_texto:
        return JsonResponse({'status': 'erro', 'message': 'Dados incompletos.'}, status=400)

    try:
        funcionario = FuncionarioProducao.objects.get(id=funcionario_id)
        
        # SOLUÇÃO ALTERNATIVA: Converte usando o fuso horário correto do Django
        try:
            # O Python lê o formato "YYYY-MM-DDTHH:MM" nativamente aqui
            data_naive = datetime.fromisoformat(data_texto)
            # Torna a data consciente do fuso horário (evita avisos de Runtime no terminal)
            data_obj = timezone.make_aware(data_naive)
        except ValueError:
            return JsonResponse({'status': 'erro', 'message': 'Formato de data inválido.'}, status=400)

        os_obj = None
        if os_id and os_id.strip() != "":
            os_obj = OrdemServico.objects.filter(rcp=os_id).first()
            if not os_obj:
                os_obj = OrdemServico.objects.filter(os=os_id).first()
            if not os_obj:
                return JsonResponse({'status': 'erro', 'message': 'Ordem de Serviço ou RCP não encontrada.'}, status=400)

        # Salva o registro
        RegistroPecaMatada.objects.create(
            funcionario=funcionario,
            quantidade=int(quantidade),
            motivo=motivo,
            os_relacionada=os_obj,
            data_ocorrencia=data_obj
        )
        return JsonResponse({'status': 'sucesso', 'message': 'Registro saved successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)

@login_required
def dados_grafico_ajax(request):
    # Agrupa o total de peças matadas por funcionário
    dados = (
        RegistroPecaMatada.objects.values('funcionario__nome')
        .annotate(total_perdas=Sum('quantidade'))
        .order_by('-total_perdas')
    )
    
    labels = [item['funcionario__nome'] for item in dados]
    valores = [item['total_perdas'] for item in dados]
    
    return JsonResponse({
        'labels': labels,
        'valores': valores
    })


@login_required
@require_POST
def adicionar_funcionario_ajax(request):
    nome = request.POST.get('nome')
    if nome:
        # Preenchemos o campo 'criado_em' manualmente com a data de agora
        FuncionarioProducao.objects.create(
            nome=nome,
            criado_em=timezone.now() 
        )
        return JsonResponse({'status': 'sucesso'})
    return JsonResponse({'status': 'erro', 'message': 'Nome inválido'}, status=400)
import traceback

@login_required
def historico_funcionario_ajax(request, funcionario_id):
    try:
        perdas = RegistroPecaMatada.objects.filter(funcionario_id=funcionario_id)\
            .annotate(data_texto=Cast('data_ocorrencia', output_field=CharField()))\
            .values('data_texto', 'os_relacionada__rcp', 'quantidade', 'motivo', 'id', 'resolucao')\
            .order_by('-id')
        
        historico_dados = []
        for p in perdas:
            data_exibicao = 'Sem data'
            data_bruta = p.get('data_texto')
            
            if data_bruta:
                dt_str = data_bruta.strip()
                try:
                    if ' ' in dt_str:
                        dt_obj = datetime.strptime(dt_str[:16], '%Y-%m-%d %H:%M')
                        data_exibicao = dt_obj.strftime('%d/%m/%Y às %H:%M')
                    else:
                        dt_obj = datetime.strptime(dt_str, '%Y-%m-%d')
                        data_exibicao = dt_obj.strftime('%d/%m/%Y')
                except Exception:
                    data_exibicao = dt_str

            historico_dados.append({
                'id': p.get('id'),  # 💡 IMPORTANTE: Adicionado para o JS saber quem editar
                'data': data_exibicao,
                'rcp': p.get('os_relacionada__rcp') or 'N/A', 
                'rcp_id': p.get('os_relacionada__id'),
                'quantidade': p.get('quantidade'),
                'motivo': p.get('motivo') or 'Não informado',
                'resolucao': p.get('resolucao') or 'Pendente'
            })
            
        return JsonResponse({'status': 'sucesso', 'historico': historico_dados})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)
    

from .models import RegistroPecaMatada, FotoPecaMatada # Importe o novo modelo

def fotos_peca_matada_modal(request, id_registro):
    # 1. Busca o registro
    registro = get_object_or_404(RegistroPecaMatada, pk=id_registro)
    
    if request.method == 'POST':
        print(f"--- DEBUG POST: Iniciando salvamento para registro {id_registro} ---")
        arquivo = request.FILES.get('foto_upload')
        
        if arquivo:
            print(f"Arquivo recebido: {arquivo.name}")
            try:
                # Chama a função que salva na rede
                caminho_no_servidor = salvar_foto_rede(arquivo, registro.os_relacionada, 'Fotos_Perdas')
                print(f"Caminho retornado pela função: {caminho_no_servidor}")
                
                # Salva no Banco
                nova_foto = FotoPecaMatada.objects.create(
                    registro=registro, 
                    imagem=caminho_no_servidor
                )
                print(f"Objeto FotoPecaMatada criado com ID: {nova_foto.id}")
                messages.success(request, "Foto salva!")
            except Exception as e:
                print(f"!!! ERRO CRÍTICO AO SALVAR: {e}")
                messages.error(request, f"Erro: {e}")
        else:
            print("!!! ERRO: Nenhum arquivo foi enviado no POST")
            
        return redirect('fotos_peca_matada_modal', id_registro=id_registro)

    # 2. Lógica do GET (Exibição)
    # AQUI ESTÁ O PULO DO GATO: Se isso retornar vazio, a tela não mostrará nada
    fotos = registro.fotos.all() 
    print(f"--- DEBUG GET: Fotos encontradas no banco para este registro: {fotos.count()} ---")
    for f in fotos:
        print(f"Foto ID {f.id} aponta para: {f.imagem}")

    return render(request, 'producao/fotos_matada_content.html', {
        'registro': registro,
        'fotos': fotos
    })

    
@login_required
def editar_motivo_ajax(request):
    try:
        perda_id = request.POST.get('perda_id')
        novo_motivo = request.POST.get('motivo')
        
        registro = RegistroPecaMatada.objects.get(id=perda_id)
        
        # O segredo: Não alteramos campos de data aqui, 
        # mas se o Django estiver disparando um 'auto_now', 
        # ele tentará atualizar a data agora. 
        # Vamos apenas garantir que o motivo seja uma string limpa.
        registro.motivo = str(novo_motivo).strip()
        
        # Força o salvamento garantindo que o fuso horário atual seja respeitado
        registro.save()
        
        return JsonResponse({'status': 'sucesso'})
        
    except Exception as e:
        # Se o erro persistir, o print abaixo no seu terminal 
        # nos dirá exatamente em qual campo ele está falhando
        print(f"DEBUG ERROR: {type(e).__name__} - {str(e)}")
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)
    
def editar_usuario_ajax(request):
    try:
        user_id = request.POST.get('id')
        novo_nome = request.POST.get('nome')
        
        # Ajustado para usar a classe correta
        func = FuncionarioProducao.objects.get(id=user_id)
        
        # Ajuste aqui: se o campo no seu model se chama 'nome', use 'func.nome'.
        # Se o campo se chama 'funcionario', use 'func.funcionario = novo_nome'
        func.nome = novo_nome 
        func.save()
        
        return JsonResponse({'status': 'sucesso'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)

@require_POST
def excluir_usuario_ajax(request):
    try:
        user_id = request.POST.get('id')
        func = FuncionarioProducao.objects.get(id=user_id)
        func.delete() # Lembre-se: se usar Soft Delete, aqui seria func.ativo = False; func.save()
        return JsonResponse({'status': 'sucesso'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)

def servir_foto_peca_matada(request, foto_id):
    foto = get_object_or_404(FotoPecaMatada, pk=foto_id)
    caminho_arquivo = foto.imagem  # O caminho completo na rede (\\servinox\...)
    
    if os.path.exists(caminho_arquivo):
        # FileResponse é perfeito para isso, pois é eficiente e cuida dos headers
        return FileResponse(open(caminho_arquivo, 'rb'))
    else:
        # Se o arquivo não existir na rede, retorna 404
        raise Http404("Arquivo não encontrado no servidor de rede.")
    

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import RegistroPecaMatada, FotoPecaMatada  # Certifique-se de importar o nome exato do seu model

def carregar_modal_edicao(request, perda_id):
    # Usamos o model correto aqui: RegistroPecaMatada
    registro = get_object_or_404(RegistroPecaMatada, id=perda_id)
    
    # IMPORTANTE: Verifique se o campo no seu model FotoPecaMatada chama-se 'registro' 
    # ou 'perda'. Ajuste o nome abaixo para corresponder ao que está no seu models.py
    fotos = FotoPecaMatada.objects.filter(registro=registro) 
    
    return render(request, 'producao/modal_perda_conteudo.html', {
        'registro': registro, 
        'fotos': fotos
    })

def atualizar_perda_ajax(request, perda_id):
    if request.method == 'POST':
        registro = get_object_or_404(RegistroPecaMatada, id=perda_id)
        
        # Atualiza os dados usando os nomes dos campos que você definiu
        registro.quantidade = request.POST.get('quantidade')
        registro.resolucao = request.POST.get('resolucao')
        registro.save()
        
        return JsonResponse({'status': 'sucesso'})
    return JsonResponse({'status': 'erro', 'message': 'Método inválido'}, status=400)