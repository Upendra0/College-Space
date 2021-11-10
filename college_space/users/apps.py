''' User App configuration '''

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self) -> None:
        #Signals to auto delete user's profile_pic.
        import users.signals
        return super().ready()
