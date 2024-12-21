from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe

# Register your models here.
class CustomAdmin(admin.ModelAdmin):
    actions = ('activate', 'desactivate')
    list_filter = ('status',)
    list_per_page = 10
    date_hierarchy = "date_add"

    def activate(self, request, queryset):
        if queryset.exists():
            queryset.update(status=True)
            self.message_user(request, 'La sélection a été activée avec succès.')
        else:
            self.message_user(request, 'Aucune sélection à activer.', level='error')
    activate.short_description = "Activer les éléments sélectionnés"

    def desactivate(self, request, queryset):
        if queryset.exists():
            queryset.update(status=False)
            self.message_user(request, 'La sélection a été désactivée avec succès.')
        else:
            self.message_user(request, 'Aucune sélection à désactiver.', level='error')
    desactivate.short_description = "Désactiver les éléments sélectionnés"

class StudentAdmin(CustomAdmin):
    list_display = ('user', 'classe', 'image_view', 'status')
    list_display_links = ['user']
    search_fields = ('user__username',)
    ordering = ('user',)
    fieldsets = [
        ("Informations sur l'élève", {"fields": ["user", "classe", "photo"]}),
        ("Statut", {"fields": ["status"]}),
    ]

    def image_view(self, obj):
        if obj.photo and hasattr(obj.photo, 'url'):
            return mark_safe(f"<img src='{obj.photo.url}' width='100px' height='50px'>")
        return "Pas d'image"
    image_view.short_description = "Photo"

class StudentReponseAdmin(CustomAdmin):
    list_display = ('student', 'response_text', 'status')
    list_display_links = ['student']
    search_fields = ('student__user__username',)
    ordering = ('student',)
    fieldsets = [
        ("Informations sur la réponse", {"fields": ["student", "response_text"]}),
        ("Statut", {"fields": ["status"]}),
    ]

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(models.Student, StudentAdmin)
_register(models.StudentReponse, StudentReponseAdmin)



