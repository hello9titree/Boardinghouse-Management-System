from django.apps import AppConfig


class BoardinghouseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boardinghouse'
    
    def ready(self):
        #Import the signals module
        import boardinghouse.signals
