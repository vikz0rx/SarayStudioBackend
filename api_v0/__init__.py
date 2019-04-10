from django.apps import AppConfig

class AuthenticationAppConfig(AppConfig):
    name = 'api_v0'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import main.signals
        
default_app_config = 'api_v0.AuthenticationAppConfig'