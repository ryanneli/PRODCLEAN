from django.contrib import admin
from .models import OrdemServico, RcpFoto, GrupoChat, Mensagem
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin

# 1. Configuração das fotos inline
class RcpFotoInline(admin.TabularInline):
    model = RcpFoto
    extra = 1

# 2. Configuração do Chat (CORRIGIDO)
class GrupoChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'criado_em')
    filter_horizontal = ('membros',) # Facilita adicionar pessoas ao grupo

admin.site.register(GrupoChat, GrupoChatAdmin)
admin.site.register(Mensagem)

# 3. Configuração da Ordem de Serviço (RCP)
class OrdemServicoAdmin(SimpleHistoryAdmin):
    inlines = [RcpFotoInline]
    # ... adicione aqui seus list_display, search_fields, etc da RCP ...

    def save_related(self, request, form, formsets, change):
        try:
            super().save_related(request, form, formsets, change)
        except OrdemServico.DoesNotExist:
            obj = form.instance
            for formset in formsets:
                for inline_form in formset:
                    if inline_form.cleaned_data and not inline_form.cleaned_data.get('DELETE'):
                        child_obj = inline_form.save(commit=False)
                        setattr(child_obj, formset.fk.name, obj)
                        child_obj.save()

# Registro da OrdemServico com a classe correta
admin.site.register(OrdemServico, OrdemServicoAdmin)

# 4. Configuração das fotos individuais
@admin.register(RcpFoto)
class RcpFotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'rcp', 'imagem', 'data_upload')
    list_filter = (('data_upload', DateRangeFilter),)
    search_fields = ('rcp__rcp', 'rcp__cliente')

# Log de histórico
admin.site.register(OrdemServico.history.model)