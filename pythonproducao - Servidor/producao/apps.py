from django.apps import AppConfig


class ProducaoConfig(AppConfig):
    name = 'producao'
    def ready(self):
        import producao.signals
    