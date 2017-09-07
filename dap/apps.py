from django.apps import AppConfig


class DapConfig(AppConfig):
    name = 'dap'

    def ready(self):
        super(DapConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('dap')
