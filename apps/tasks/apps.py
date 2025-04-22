from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = "eTaskify.apps.tasks"
    verbose_name = _("task")
