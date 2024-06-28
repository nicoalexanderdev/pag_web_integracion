from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PassValidator:
    def validate(self, password, user=None):
        pass

    def get_help_text(self):
        return _('No hay restricciones para la contraseña.')

