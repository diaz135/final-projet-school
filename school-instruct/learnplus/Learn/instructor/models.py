from django.db import models
from django.contrib.auth.models import User
from school import models as school_models
from django.utils.text import slugify
from quiz import models as quiz_models


# Create your models here.
class Instructor(models.Model):
    user = models.OneToOneField(User, related_name='instructor', on_delete=models.CASCADE)
    contact = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    classe = models.ForeignKey('school.Classe', related_name='instructor_classe', on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='images/Instructor')
    bio = models.TextField(default="Votre bio")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    matieres = models.ManyToManyField('school.Matiere', related_name='instructors',
                                      blank=True)  # Relation Many-to-Many avec Matiere
    questions = models.ManyToManyField(quiz_models.Question, related_name='instructeur', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Instructor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self):
        return self.user.username

    @property
    def get_u_type(self):
        try:
            user = User.objects.get(id=self.user.id)
            cheick = user.instructor
            return True
        except BaseException:
            return False
