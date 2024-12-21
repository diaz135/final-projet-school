from django.db import models
from django.contrib.auth.models import User
from school import models as school_models
from quiz import models as quiz_models
from django.utils.text import slugify


# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User,related_name='student_user',on_delete=models.CASCADE)
    classe = models.ForeignKey(school_models.Classe,on_delete=models.CASCADE,related_name='student_classe', null=True)
    photo = models.ImageField(upload_to='images/Student')
    bio = models.TextField(default="Votre bio")
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True,  blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Student, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username

    @property
    def get_u_type(self):
        try:
            user = User.objects.get(id=self.user.id)
            cheick = user.student_user
            return True
        except:
            return False

class StudentReponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="responses")
    response_text = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Student Response"
        verbose_name_plural = "Student Responses"

    def __str__(self):
        return f"{self.student.user.username} - {self.response_text[:20]}"
