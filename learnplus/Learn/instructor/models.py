from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from school import models as school_models


# Modèle Instructor
class Instructor(models.Model):
    user = models.OneToOneField(User, related_name='instructor', on_delete=models.CASCADE)
    contact = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    classe = models.ForeignKey(
        "school.Classe",  # Utilisation d'une chaîne pour éviter l'importation directe
        related_name='instructor_classe',
        on_delete=models.CASCADE,
        null=True
    )
    photo = models.ImageField(upload_to='images/Instructor')
    bio = models.TextField(default="Votre bio")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    matieres = models.ManyToManyField(school_models.Matiere, related_name='instructors', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Instructor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self):
        return self.user.username


# Modèle AffectationMatiere
class AffectationMatiere(models.Model):
    instructor = models.ForeignKey(
        "instructor.Instructor",  # Référence à l'instructeur via une chaîne
        on_delete=models.CASCADE,
        related_name="affectations"
    )
    matiere = models.ForeignKey(
        "school.Matiere",  # Référence à Matiere via une chaîne
        on_delete=models.CASCADE,
        related_name="affectations"
    )
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Affectation de Matière"
        verbose_name_plural = "Affectations de Matières"
        unique_together = ("instructor", "matiere")  # Empêche la duplication d'affectations

    def __str__(self):
        return f"{self.instructor.user.username} - {self.matiere.nom}"
