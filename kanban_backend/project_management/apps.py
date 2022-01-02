from django.apps import AppConfig


class ProjectManagementConfig(AppConfig):
    name = 'kanban_backend.project_management'

    def ready(self):
        try:
            import kanban_backend.users.signals  # noqa F401
        except ImportError:
            pass

