from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save)
def rastrear_mudancas_obs(sender, instance, **kwargs):
    # AJUSTE: O nome do model é OrdemServico
    if sender.__name__ != 'OrdemServico':
        return

    if instance.pk:
        # Import local correto
        from .models import OrdemServico
        try:
            anterior = OrdemServico.objects.get(pk=instance.pk)
            instance._obs_qualidade_antiga = anterior.obs_qualidade
            instance._obs_comercial_antiga = anterior.observacao_comercial
            instance._obs_producao_antiga = anterior.obs_producao
        except OrdemServico.DoesNotExist:
            pass
    else:
        instance._obs_qualidade_antiga = ""
        instance._obs_comercial_antiga = ""
        instance._obs_producao_antiga = ""

@receiver(post_save)
def disparar_notificacoes(sender, instance, created, **kwargs):
    if sender.__name__ != 'OrdemServico' or created:
        return

    from .models import NotificacaoSetor
    
    # Mapeamento dos campos de observação
    campos_obs = [
        ('obs_qualidade', '_obs_qualidade_antiga', 'QUALIDADE'),
        ('observacao_comercial', '_obs_comercial_antiga', 'COMERCIAL'),
        ('obs_producao', '_obs_producao_antiga', 'PRODUÇÃO'),
    ]

    setores_destino = ['COMERCIAL', 'QUALIDADE', 'PRODUCAO', 'ADMIN']

    for campo, attr_antigo, nome_setor_mudanca in campos_obs:
        # Pega o valor atual e o antigo (salvo no pre_save)
        valor_atual = getattr(instance, campo, "")
        valor_antigo = getattr(instance, attr_antigo, "")

        if valor_atual != valor_antigo:
            # Mensagem usando o campo correto da OrdemServico: instance.rcp
            msg = f"A RCP {instance.rcp} teve a observação da {nome_setor_mudanca} alterada."
            
            for setor in setores_destino:
                NotificacaoSetor.objects.create(
                    setor_destino=setor,
                    mensagem=msg,
                    # De instance.rcp para o campo rcp_numero do model NotificacaoSetor
                    rcp_numero=instance.rcp 
                )