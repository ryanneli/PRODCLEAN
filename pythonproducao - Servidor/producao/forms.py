from django import forms
from .models import OrdemServico

class RCPForm(forms.ModelForm):
    # Forçamos a RCP como IntegerField aqui para o Django aceitar sua edição manual,
    # mesmo que no Models seja um AutoField.
    rcp = forms.IntegerField(
        label="Número da RCP",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = OrdemServico
        fields = '__all__'
        widgets = {
            'data_entrada_peca': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}),
            'previsao_entrega_qualidade': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
            'data_expedicao': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
            'previsao_conclusao_prod': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
            'data_liberacao': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}),
            'inicio_producao': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}),
            'data_finaliza_producao': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}),
            'descricao_peca': forms.Textarea(attrs={'rows': 4}),
            'obs_qualidade': forms.Textarea(attrs={'rows': 5}),
            'obs_producao': forms.Textarea(attrs={'rows': 5}),
            'data_inspecao_final': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}),
            'data_inspecao_inicial': forms.DateTimeInput(format = '%Y-%m-%dT%H:%M',attrs={'type': 'datetime-local'}),
            'obs_expedicao': forms.Textarea(attrs={'rows': 4}),
            'certificado_pdf': forms.FileInput(attrs={'class': 'form-control','accept': '.pdf'}),
            'nome_motorista': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # Diminui a altura para 3 linhas
                'style': 'resize: vertical;' # Opcional: impede o usuário de puxar e aumentar
            }),
            'observacao_comercial': forms.Textarea(attrs={'rows': 5, 'style': 'resize: vertical;'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 1. Definição das listas de campos
        campos_comercial = ['os', 'proposta', 'nf_saida', 'tipo_servico', 'prioridade', 'liberado_por','data_liberacao', 'observacao_comercial']
        campos_qualidade = ['rcp', 'cliente', 'nf_cliente', 'data_entrada_peca', 'descricao_peca', 'obs_qualidade', 'previsao_entrega_qualidade', 'data_expedicao', 'expedido_por', "data", "data_inspecao_final", 'data_inspecao_inicial', 'nome_motorista', 'placa_veiculo', 'obs_expedicao']
        campos_producao = ['status', 'inicio_producao', 'operador', 'previsao_conclusao_prod', 'data_finaliza_producao', 'obs_producao']
        self.fields['liberado_por'].disabled = True
        self.fields['status'].disabled = True
        if user and not user.groups.filter(name='Comercial').exists():
            self.fields['prioridade'].disabled = True
        # 2. Aplicar Estilo Bootstrap e recuperar o layout "sem scroll"
        for field_name, field in self.fields.items():
            # Mantemos a classe form-control para o layout ficar alinhado
            field.widget.attrs.update({'class': 'form-control'})

        # 3. Lógica de Bloqueio por Grupo (Acumulativa)
        if user and not user.is_superuser:
            pode_comercial = user.groups.filter(name='Comercial').exists()
            pode_qualidade = user.groups.filter(name='Qualidade').exists()
            pode_producao = user.groups.filter(name='Producao').exists()

            if not pode_comercial: self.travar_setor(campos_comercial)
            if not pode_producao: self.travar_setor(campos_producao)
            if not pode_qualidade:
                outros_qualidade = [f for f in campos_qualidade if f != 'rcp']
                self.travar_setor(outros_qualidade)

        # 4. TRATAMENTO FINAL RCP (Editável na criação, travada na edição)
        if not self.instance.pk:
            self.fields['rcp'].widget.attrs.update({
                'class': 'form-control bg-white fw-bold border-primary',
                'readonly': False
            })
        else:
            self.fields['rcp'].widget.attrs.update({
                'readonly': 'readonly',
                'class': 'form-control bg-light'
            })

    def travar_setor(self, lista):
        for campo in lista:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = 'readonly'
                self.fields[campo].widget.attrs.update({'class': 'form-control bg-light'})

    # Garante que o número digitado seja salvo mesmo sendo AutoField
    def clean_rcp(self):
        return self.cleaned_data.get('rcp')