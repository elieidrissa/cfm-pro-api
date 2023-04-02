from django.apps import AppConfig


class CfmProApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cfm_pro_api'

    def ready(self):
        import cfm_pro_api.signals
