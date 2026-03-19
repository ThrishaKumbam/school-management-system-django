from django.apps import AppConfig


class SchoolSystemAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school_system_app'

    def ready(self):
        import school_system_app.signals