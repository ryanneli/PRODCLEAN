from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import Mensagem

def chat_context_processor(request):
    if not request.user.is_authenticated:
        return {
            'todos_usuarios': [],
            'total_nao_lidas_global': 0,
            'meus_grupo_ids': []
        }

    try:
        # 1. IDs dos grupos para o WebSocket global
        grupo_ids = list(request.user.meus_grupos_chat.values_list('id', flat=True))
        
        # 2. Busca os usuários trazendo junto a contagem de não lidas que CADA UM enviou para o usuário logado
        # Nota: Ajuste 'mensagem' se o related_name no seu model Mensagem for diferente
        usuarios = User.objects.exclude(id=request.user.id).annotate(
            mensagens_nao_lidas=Count(
                'mensagem',  
                filter=Q(
                    mensagem__lida=False,
                    mensagem__grupo__membros=request.user
                )
            )
        ).order_by('username')

        # 3. Total global (soma das mensagens não lidas de todos os usuários anotados)
        total_global = sum(u.mensagens_nao_lidas for u in usuarios)

        return {
            'todos_usuarios': usuarios,
            'total_nao_lidas_global': total_global,
            'meus_grupo_ids': grupo_ids
        }

    except Exception as e:
        # Log simplificado para debug se necessário, sem travar a aplicação
        print(f"Erro no Context Processor do Chat: {e}")
        return {
            'todos_usuarios': [],
            'total_nao_lidas_global': 0,
            'meus_grupo_ids': []
        }