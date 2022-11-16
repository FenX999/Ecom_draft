from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yuugen.apps.users'
    # def ready(self):
    #     import yuugen.apps.core.signals
