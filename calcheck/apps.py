from django.apps import AppConfig
from ml_model.detect import CalcheckModel


class CalcheckConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calcheck"

    model = CalcheckModel()
