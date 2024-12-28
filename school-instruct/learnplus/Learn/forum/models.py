from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime


class Sujet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sujet')
    cours = models.ForeignKey('school.Cours', on_delete=models.CASCADE, related_name='cours_forum', null=True)
    question = models.TextField()
    titre = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Génère le slug uniquement s'il est absent
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.slug = slugify(f"{self.titre}-{timestamp}")
        super(Sujet, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Sujet'
        verbose_name_plural = 'Sujets'
        ordering = ['-date_add']

    def __str__(self):
        return self.titre


class Reponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reponse')
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='sujet_reponse')
    contenu = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Génère le slug uniquement s'il est absent
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.slug = slugify(f"{self.sujet.titre}-{timestamp}")
        super(Reponse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Reponse"
        verbose_name_plural = "Reponses"

    def __str__(self):
        return f"Reponse by {self.user.username} on {self.sujet.titre}"
