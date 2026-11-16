from datetime import timedelta, timezone
import os
from django.db import models
from django.contrib.auth.models import User, Group  # Corrigido: Group no singular
from django.dispatch import receiver
from django.db.models.signals import post_delete
from simple_history.models import HistoricalRecords

class OrdemServico(models.Model):
    # --- OPÇÕES ---
    PRIORIDADE_CHOICES = [
        ('SEM PRIORIDADE', 'Sem Prioridade'),
        ('MODERADO', 'Moderado'),
        ('URGENTE', 'Urgente'),
        ('A SER DEFINIDO PELA COMERCIAL', 'A Ser Definido Pela Comercial'),
    ]

    STATUS_CHOICES = [
        ('AGUARDANDO LIBERAÇÃO', 'Aguardando Liberação'),
        ('EM PRODUÇÃO', 'Em Produção'),
        ('ENTREGUE AO CLIENTE', 'Entregue ao Cliente'),
        ('AGUARDANDO RETIRADA', 'Aguardando Retirada'),
        ('AGUARDANDO INSPEÇÃO FINAL', 'Aguardando Inspeção Final'),
        ('AGUARDANDO INSPEÇÃO INICIAL', 'Aguardando Inspeção Inicial'),
        ('LIBERADO PARA INSPEÇÃO', 'Liberado para Inspeção'),
        ('LIBERADO PARA PRODUÇÃO', 'Liberado para Produção'),
        ('AGUARDANDO NOTA DE SAIDA', 'Aguardando Nota de Saida'),
    ]

    # --- BLOQUEIO LÓGICO DE SESSÃO ---
    editando_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Editado atualmente por")
    editando_desde = models.DateTimeField(null=True, blank=True)
    version = models.IntegerField(default=0)

    # --- COMERCIAL ---
    os = models.CharField(max_length=20, verbose_name="OS", default="0000/26")
    cliente = models.CharField(max_length=100)
    proposta = models.CharField(max_length=50, blank=True, default='', null=True)
    nf_saida = models.CharField(max_length=50, blank=True, verbose_name="NF Saída", default='', null=True)
    tipo_servico = models.CharField(max_length=100, verbose_name="Tipo de Serviço", blank=True, null=True)
    prioridade = models.CharField(max_length=30, choices=PRIORIDADE_CHOICES, default='A SER DEFINIDO PELA COMERCIAL')
    data_liberacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Liberação")
    liberado_por = models.CharField(max_length=100, blank=True, null=True, verbose_name="Liberado Por")
    # Adicionado null=True para evitar IntegrityError no histórico
    observacao_comercial = models.TextField(null=True, blank=True, verbose_name="Observação Comercial", default='')

    # --- QUALIDADE ---
    rcp = models.IntegerField(primary_key=True, verbose_name="Número da RCP")
    nf_cliente = models.CharField(max_length=50, blank=True, verbose_name="NF do Cliente", default='', null=True)
    data_entrada_peca = models.DateTimeField(null=True, blank=True)
    descricao_peca = models.TextField(null=True, blank=True, verbose_name="Descrição da Peça", default='')
    obs_qualidade = models.TextField(null=True, blank=True, verbose_name="Observação Qualidade", default='')
    previsao_entrega_qualidade = models.DateTimeField(null=True, blank=True, verbose_name="Previsão de Entrega para Qualidade")
    data_inspecao_inicial = models.DateTimeField(null=True, blank=True, verbose_name="Data Inspeção Inicial")

    # --- EXPEDIÇÃO (QUALIDADE) ---
    nome_motorista = models.TextField(max_length=100, blank=True, verbose_name="Nome do Motorista", default='', null=True)
    placa_veiculo = models.CharField(max_length=20, blank=True, verbose_name="Placa do Veículo", default='', null=True)
    obs_expedicao = models.TextField(null=True, blank=True, verbose_name="Observação Expedição", default='')  
    data_expedicao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Expedição")  
    expedido_por = models.CharField(max_length=50, blank=True, default='', null=True)

    # --- PRODUÇÃO ---
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='AGUARDANDO LIBERAÇÃO')
    inicio_producao = models.DateTimeField(null=True, blank=True, verbose_name="Início da Produção")
    operador = models.CharField(max_length=200, blank=True, default='', null=True)
    previsao_conclusao_prod =models.DateTimeField(null=True, blank=True, verbose_name="Previsão de Conclusão da Produção")
    data_finaliza_producao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Finalização da Produção")
    # Adicionado null=True para consistência
    obs_producao = models.TextField(null=True, blank=True, verbose_name="Observação da Produção", default='')
    data_inspecao_final = models.DateTimeField(null=True, blank=True, verbose_name="Data Inspeção Final")

    certificado_pdf = models.FileField(upload_to='certificados/%Y/%m/', null=True, blank=True, verbose_name="Certificado de Qualidade")

    def pode_editar(self, usuario):
        # Se ninguém estiver editando, está livre
        if not self.editando_por:
            return True
        # Se o usuário for o próprio que já está editando, está livre
        if self.editando_por == usuario:
            return True
        # Se o tempo de "trava" (ex: 30 min) expirou, libera para outro
        if self.editando_desde and timezone.now() > self.editando_desde + timedelta(minutes=30):
            return True
        return False

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
       if self.data_expedicao:
        self.status = "ENTREGUE AO CLIENTE"

        # 2. EXPEDIÇÃO (Peça pronta, mas e a nota?)
       elif self.data_inspecao_final and self.data_finaliza_producao:
            if not self.nf_saida or str(self.nf_saida).strip() == "":
                self.status = "AGUARDANDO NOTA DE SAIDA"
            else:
                self.status = "AGUARDANDO RETIRADA"

        # 3. QUALIDADE FINAL
       elif self.data_finaliza_producao:
            self.status = "AGUARDANDO INSPEÇÃO FINAL"

        # 4. PRODUÇÃO
       elif self.inicio_producao:
            self.status = "EM PRODUÇÃO"

        # 5. INSPEÇÃO INICIAL / LIBERAÇÃO (Fluxo de Entrada)
       elif self.data_liberacao:
            if self.data_inspecao_inicial:
                self.status = "LIBERADO PARA PRODUÇÃO"
            else:
                self.status = "AGUARDANDO INSPEÇÃO INICIAL"

        # 6. STATUS PADRÃO (Início de tudo)
       else:
            self.status = "AGUARDANDO LIBERAÇÃO"

        # 2. Só atualiza o campo se ele mudou (evita disparar o Histórico à toa)
       super().save(*args, **kwargs)

    def __str__(self):
        return f"RCP {self.rcp} - {self.cliente}"



class QuadroObras(models.Model):
    os_obra = models.IntegerField(primary_key=True, verbose_name="Número da OS/Obra")
    cliente = models.CharField(max_length=100)
    descricao_obra = models.TextField(null=True, blank=True, verbose_name="Descrição daObra", default='')
    data_inicio_obra = models.DateField(null=True, blank=True, verbose_name="Data de Início da Obra")



class CertificadoRCP(models.Model):
    rcp = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='certificados')
    arquivo = models.FileField(upload_to='certificados/%Y/%m/')
    nome_exibicao = models.CharField(max_length=255, blank=True) # Para salvar o nome original do arquivo
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_exibicao or f"Certificado {self.id}"




class RcpFoto(models.Model):
    rcp = models.ForeignKey(OrdemServico, related_name='fotos', on_delete=models.CASCADE)
    
    # ALTERADO: De ImageField para CharField para aceitar o caminho de rede puro
    imagem = models.CharField(max_length=500) 
    
    data_upload = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(
        max_length=10, 
        choices=[('antes', 'Antes'), ('apos', 'Após')], 
        default='antes'
    )

    def __str__(self):
        return f"Foto {self.tipo} da RCP {self.rcp.rcp}"

class NotificacaoSetor(models.Model):
    SETOR_CHOICES = [
        ('COMERCIAL', 'Comercial'),
        ('QUALIDADE', 'Qualidade'),
        ('PRODUCAO', 'Produção'),
        ('ADMIN', 'Administrador'),
    ]
    setor_destino = models.CharField(max_length=20, choices=SETOR_CHOICES)
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    rcp_numero = models.CharField(max_length=50)
    
    # Em vez de um Boolean, usamos uma relação com os usuários
    usuarios_que_leram = models.ManyToManyField(
        User, 
        related_name='notificacoes_lidas', 
        blank=True
    )

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"Notificação {self.rcp_numero} - {self.setor_destino}"

# --- SIGNALS ---
@receiver(post_delete, sender=RcpFoto)
def apagar_imagem_arquivo(sender, instance, **kwargs):
    # Como agora é um CharField, o instance.imagem é apenas uma string com o caminho
    if instance.imagem:
        caminho = str(instance.imagem)
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
                print(f"Arquivo removido da rede: {caminho}")
            except Exception as e:
                print(f"Erro ao deletar arquivo físico: {e}")

from django.contrib.auth.models import User
from django.utils import timezone

class GrupoChat(models.Model):
    nome = models.CharField(max_length=150, blank=True, null=True)
    membros = models.ManyToManyField(User, related_name='meus_grupos_chat')
    criado_em = models.DateTimeField(auto_now_add=True)
    e_grupo = models.BooleanField(default=False) # True = Grupo, False = Chat Privado 1x1

    def __str__(self):
        return self.nome if self.nome else f"Chat {self.id}"

    @staticmethod
    def obter_ou_criar_privado(user1, user2):
        """
        Busca um chat privado entre dois usuários. Se não existir, cria um.
        """
        # Busca grupos que não são 'e_grupo' e que contêm ambos os usuários
        qs = GrupoChat.objects.filter(e_grupo=False).filter(membros=user1).filter(membros=user2)
        
        # Garante que o chat tenha EXATAMENTE 2 membros (os dois interessados)
        for chat in qs:
            if chat.membros.count() == 2:
                return chat
        
        # Se não achou, cria um novo
        novo_chat = GrupoChat.objects.create(e_grupo=False, nome=f"Privado: {user1.username} & {user2.username}")
        novo_chat.membros.add(user1, user2)
        return novo_chat

class Mensagem(models.Model):
    grupo = models.ForeignKey(GrupoChat, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    editada = models.BooleanField(default=False)
    data_edicao = models.DateTimeField(null=True, blank=True)
    lida = models.BooleanField(default=False)
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.autor.username}: {self.texto[:20]}"

class LogEdicaoMensagem(models.Model):
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE, related_name='historico_edicoes')
    texto_antigo = models.TextField()
    data_alteracao = models.DateTimeField(auto_now_add=True)

#pagina peças matadas
class FuncionarioProducao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.nome

class RegistroPecaMatada(models.Model):
    funcionario = models.ForeignKey(FuncionarioProducao, on_delete=models.CASCADE, related_name='perdas')
    quantidade = models.PositiveIntegerField()
    data_ocorrencia = models.DateTimeField(blank=False, null=False)
    motivo = models.CharField(max_length=255, blank=True, null=True)   
    resolucao = models.TextField(verbose_name="Resolução", blank=True, null=True) 
    # NOVO CAMPO AQUI:
    os_relacionada = models.ForeignKey('OrdemServico', on_delete=models.SET_NULL, null=True, blank=True, related_name='perdas_pecas')

    def __str__(self):
        return f"{self.quantidade} pçs - {self.funcionario.nome}"
    
class FotoPecaMatada(models.Model):
    # Relaciona com o registro da perda específica
    registro = models.ForeignKey(RegistroPecaMatada, related_name='fotos', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, null=True, blank=True)
    # Mantendo o padrão que você usa (CharField para caminho de rede)
    imagem = models.CharField(max_length=500) 
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto da peça matada (Registro {self.registro.id})"