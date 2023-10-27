from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=255)

class Ability(models.Model):
    name = models.CharField(max_length=255)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)