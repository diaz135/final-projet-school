from django.db import models
from django.utils.text import slugify
from datetime import datetime

# Create your models here.
class Filiere(models.Model):
    nom = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Filiere'
        verbose_name_plural = 'Filieres'

    def str(self):
        return self.nom

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/matiere/", null=True)
    description = models.TextField(default="Description du cours")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True,  blank=True)

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.nom), slugify(self.date_add)))
        super(Matiere, self).save(*args, **kwargs)
    


    class Meta:
        verbose_name = 'Matiere'
        verbose_name_plural = 'Matieres'

    def str(self):
        return self.nom

class Niveau(models.Model):
    nom = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True,  blank=True)

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.nom), slugify(self.date_add)))
        super(Niveau, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Niveau'
        verbose_name_plural = 'Niveaux'

    def str(self):
        return self.nom

class Classe(models.Model):
    niveau = models.ForeignKey(Niveau,on_delete=models.CASCADE,related_name='classe_niveau')
    numeroClasse = models.IntegerField()
    filiere = models.ForeignKey(Filiere,on_delete=models.CASCADE,related_name='classe_filiere',null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    


    class Meta:
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'

    def str(self):
        return (str(self.niveau.nom)+ " "+ str(self.numeroClasse))
 
class Chapitre(models.Model):
    
    classe = models.ForeignKey(Classe,on_delete=models.CASCADE,related_name='classe_chapitre', null=True)
    matiere = models.ForeignKey(Matiere,on_delete=models.CASCADE,related_name='matiere_chapitre')
    video = models.FileField(upload_to="ressources/cours", null=True)
    duree_en_heure = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to="images/chapitres", null=True)
    description = models.TextField(default="Description du chapitre")
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)
    titre = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True,  blank=True)

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.titre), slugify(self.date_add)))
        super(Chapitre, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Chapitre'
        verbose_name_plural = 'Chapitres'

    def str(self):
        return self.titre


class Cours(models.Model):
    titre = models.CharField(max_length=255)
    chapitre = models.ForeignKey(Chapitre,on_delete=models.CASCADE,related_name='cours_chapitre')
    image = models.ImageField(upload_to='images/cours' , null=True)
    video = models.FileField(upload_to="ressources/cours",null=True)
    pdf = models.FileField(upload_to="ressources/cours", null=True)
    description = models.TextField(default="Description du cours")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True,  blank=True)

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.titre), slugify(self.date_add)))
        super(Cours, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def str(self):
        return self.titre