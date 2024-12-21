from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Instructor, AffectationMatiere


class CustomAdmin(admin.ModelAdmin):
    """
    Base admin class pour les fonctionnalités réutilisables.
    """
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, 'Les éléments sélectionnés ont été activés avec succès.')
    activate.short_description = "Activer les éléments sélectionnés"

    def deactivate(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, 'Les éléments sélectionnés ont été désactivés avec succès.')
    deactivate.short_description = "Désactiver les éléments sélectionnés"


@admin.register(Instructor)
class InstructorAdmin(CustomAdmin):
    list_display = ('user', 'contact', 'adresse', 'image_view', 'classe', 'matieres_list', 'status')
    search_fields = ('user__username', 'contact', 'adresse')
    ordering = ['user']
    list_display_links = ['user']
    list_filter = ('classe', 'status')
    fieldsets = [
        ("Informations sur l'instructeur", {"fields": ["user", "contact", "adresse", "classe", "photo", "matieres"]}),
        ("Statut", {"fields": ["status"]}),
    ]

    def image_view(self, obj):
        """
        Affiche une image dans l'admin si disponible.
        """
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='100px' height='50px'>")
        return "Pas d'image"

    image_view.short_description = "Photo"

    def matieres_list(self, obj):
        """
        Affiche une liste des matières attribuées à l'instructeur.
        """
        return ", ".join([matiere.nom for matiere in obj.matieres.all()])

    matieres_list.short_description = "Matières"


@admin.register(AffectationMatiere)
class AffectationMatiereAdmin(CustomAdmin):
    list_display = ('instructor', 'matiere', 'date_add', 'date_update')
    search_fields = ('instructor__user__username', 'matiere__nom')
    list_filter = ('date_add', 'date_update')
    ordering = ['instructor', 'matiere']
