from re import compile as recompile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PassValidator:
    pin_regex = recompile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

    def validate(self, password, user=None):
        if not self.pin_regex.fullmatch(password):
            raise ValidationError(
                _('La contraseña debe contener al menos 8 caracteres, incluyendo al menos un número y una letra.'),
                code='invalid_password',
            )

    def get_help_text(self):
        return _('La contraseña debe contener al menos 8 caracteres, incluyendo al menos un número y una letra.')
