from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['firstname_len'] = "El nombre debe tener al menos 2 caracteres de largo.";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Correo invalido."

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "Utilizar solo letras en nombre porfavor."

        if len(postData['password']) < 4:
            errors['password'] = "La contraseña debe contener al menos 8 caracteres.";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no coinciden. "

        
        return errors


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.URLField(max_length=1000)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

class Trips(models.Model):
    place = models.CharField(max_length=250)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField ()
    plan = models.TextField (max_length=250)
    created_by = models.ForeignKey(User,related_name="trip",on_delete=models.CASCADE)
    travellers = models.ManyToManyField(User,related_name="users_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __lt__(self):
        return self

    def __repr__(self):
        return f"{self.place} {self.id}"

