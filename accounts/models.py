import re
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

def validate_institutional_email(value):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(edu|edu\.[a-z]{2})$'
    if not re.match(pattern, value, re.IGNORECASE):
        ValidationError('El registro requiere un correo institucional válido (.edu / .edu.co).')

class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Estudiante'),
        ('TEACHER', 'Docente'),
        ('RESEARCHER', 'Investigador'),
        ('ADMIN', 'Administrador'),
    )
    STATUS_CHOICES = (
        ('ACTIVE', 'Activo'),
        ('SUSPENDED', 'Suspendido'),
    )

    username = None
    email = models.EmailField(unique=True, validators=[validate_institutional_email])
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"