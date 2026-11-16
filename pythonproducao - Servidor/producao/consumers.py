import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import GrupoChat, Mensagem

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.grupo_id = self.scope['url_route']['kwargs'].get('grupo_id')
        
        # 1. Garante que o usuário está autenticado
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        # 2. Conexão do Chat (Grupo específico)
        if self.grupo_id:
            self.grupo_nome = f'chat_{self.grupo_id}'
            await self.channel_layer.group_add(self.grupo_nome, self.channel_name)
            
        # 3. Conexão para Avisos Globais (Manutenção)
        await self.channel_layer.group_add("avisos_globais", self.channel_name)
        
        await self.accept()

    async def disconnect(self, close_code):
        # Remove do grupo do chat
        if hasattr(self, 'grupo_nome'):
            await self.channel_layer.group_discard(self.grupo_nome, self.channel_name)
        
        # Remove do grupo de avisos globais
        await self.channel_layer.group_discard("avisos_globais", self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'erro': 'JSON inválido'}))
            return

        tipo = data.get('tipo', 'mensagem')

        if tipo == 'edicao':
            msg_id = data.get('msg_id')
            novo_texto = data.get('mensagem')
            
            if msg_id and novo_texto:
                await self.editar_mensagem_banco(msg_id, novo_texto)
                await self.channel_layer.group_send(
                    self.grupo_nome,
                    {
                        'type': 'chat_message_edit',
                        'msg_id': msg_id,
                        'mensagem': novo_texto
                    }
                )

        elif tipo == 'leitura':
            await self.marcar_como_lida(self.grupo_id)
            await self.channel_layer.group_send(
                self.grupo_nome,
                {
                    'type': 'chat_read_receipt',
                    'usuario_que_leu': self.scope["user"].username
                }
            )
        
        else:
            texto_mensagem = data.get('mensagem')
            if not texto_mensagem:
                return

            msg_obj = await self.salvar_mensagem(self.grupo_id, texto_mensagem)
            
            if msg_obj:
                await self.channel_layer.group_send(
                    self.grupo_nome,
                    {
                        'type': 'chat_message',
                        'msg_id': msg_obj.id,
                        'mensagem': texto_mensagem,
                        'usuario': self.scope["user"].username,
                        'hora': timezone.localtime(msg_obj.data_envio).strftime('%H:%M')
                    }
                )
            else:
                await self.send(text_data=json.dumps({'erro': 'Não foi possível enviar a mensagem.'}))

    # --- HANDLERS DE MENSAGENS ---
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def chat_message_edit(self, event):
        await self.send(text_data=json.dumps(event))

    async def chat_read_receipt(self, event):
        await self.send(text_data=json.dumps(event))

    # --- HANDLER DE AVISO GLOBAL (Manutenção) ---
    async def enviar_aviso(self, event):
        await self.send(text_data=json.dumps({
            'tipo': 'manutencao',
            'mensagem': event['mensagem']
        }))

    # --- BANCO DE DADOS ---
    @database_sync_to_async
    def salvar_mensagem(self, grupo_id, texto):
        try:
            grupo = GrupoChat.objects.get(id=grupo_id)
            return Mensagem.objects.create(
                grupo=grupo,
                autor=self.scope["user"],
                texto=texto
            )
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return None

    @database_sync_to_async
    def editar_mensagem_banco(self, msg_id, texto):
        try:
            msg = Mensagem.objects.get(id=msg_id, autor=self.scope["user"])
            msg.texto = texto
            msg.editada = True
            msg.data_edicao = timezone.now()
            msg.save()
        except Exception as e:
            print(f"Erro ao editar: {e}")

    @database_sync_to_async
    def marcar_como_lida(self, grupo_id):
        from .models import Mensagem
        Mensagem.objects.filter(
            grupo_id=grupo_id, 
            lida=False
        ).exclude(autor=self.scope["user"]).update(lida=True)