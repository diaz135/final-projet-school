from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe

# Register your models here.


class CustomAdmin(admin.ModelAdmin):
    actions = ('activate','desactivate')
    list_filter = ('status',)
    list_per_page = 6
    date_hierachy = "date_add"

    def activate(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,'la selection a été effectué avec succes')
    activate.short_description = "permet d'activer le champs selectionner"

    def desactivate(self,request,queryset):
        queryset.update(status=False)
        self.message_user(request,'la selection a été effectué avec succes')
    desactivate.short_description = "permet de desactiver le champs selectionner"


class InstructorAdmin(CustomAdmin):
    list_display = ('user', 'contact', 'adresse', 'image_view', 'classe', 'matieres_list', 'status')
    search_fields = ('user',)
    ordering = ['user']
    list_display_links = ['user']
    fieldsets = [
        ("Info Instructeur", {"fields": ["user", "contact", "adresse", "classe", "photo", "matieres"]}),
        ("Standard", {"fields": ["status"]}),
    ]

    def image_view(self, obj):
        return mark_safe("<img src='{url}' width='100px' height='50px'>".format(url=obj.photo.url))

    def matieres_list(self, obj):
        return ", ".join([matiere.nom for matiere in obj.matieres.all()])
    matieres_list.short_description = "Matières"


def _register(model,admin_class):
    admin.site.register(model,admin_class)


_register(models.Instructor, InstructorAdmin)
