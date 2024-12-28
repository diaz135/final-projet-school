from django.contrib import admin
from . import models

# CustomAdmin pour des fonctionnalités partagées


class CustomAdmin(admin.ModelAdmin):
    actions = ('activate', 'desactivate')
    list_filter = ('status',)
    list_per_page = 10
    date_hierarchy = "date_add"

    def activate(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, "Les éléments sélectionnés ont été activés avec succès.")
    activate.short_description = "Activer les champs sélectionnés"

    def desactivate(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, "Les éléments sélectionnés ont été désactivés avec succès.")
    desactivate.short_description = "Désactiver les champs sélectionnés"


class QuestionAdmin(CustomAdmin):
    list_display = ('title', 'question_type', 'score', 'timeframe_enabled', 'status', 'date_add')
    search_fields = ('title',)
    list_filter = ('question_type', 'status')


class ReponseAdmin(CustomAdmin):
    list_display = ('reponse', 'question', 'is_True', 'status')
    list_display_links = ['reponse']
    search_fields = ('reponse',)
    list_editable = ('is_True', 'status')  # Ajout pour édition rapide
    fieldsets = [
        ("Info Réponse", {"fields": ["reponse", "question", "is_True"]}),
        ("Standard", {"fields": ["status"]}),
    ]


class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'instructor', 'temps', 'status', 'date_add', 'date_update')
    list_filter = ('status', 'date_add', 'date_update')  # Filtres sur le côté
    search_fields = ('titre', 'instructor__username',)  # Recherche par titre, instructeur ou cours
    prepopulated_fields = {'slug': ('titre',)}  # Génère automatiquement le slug à partir du titre
    date_hierarchy = 'date_add'  # Navigation par date dans l'admin
    readonly_fields = ('slug', 'date_add', 'date_update')  # Champs non modifiables
    autocomplete_fields = ['instructor']  # Amélioration pour les relations
    fieldsets = (
        ('Informations Générales', {
            'fields': ('titre', 'instructor', 'image', 'temps', 'status')
        }),
        ('Avancé', {
            'classes': ('collapse',),  # Section pliable
            'fields': ('slug', 'date_add', 'date_update')
        }),
    )


class DevoirAdmin(CustomAdmin):
    list_display = ('dateDebut', 'dateFermeture', 'chapitre', 'coefficient', 'support', 'status')
    list_display_links = ('chapitre',)
    search_fields = ('chapitre',)
    fieldsets = [
        ("Info Devoir", {"fields": ["dateDebut", "dateFermeture", 'chapitre', 'support']}),
        ("Standard", {"fields": ["status"]}),
    ]


# Fonction pour enregistrer les modèles
def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Question, QuestionAdmin)
_register(models.Reponse, ReponseAdmin)
admin.site.register(models.Quiz, QuizAdmin)
_register(models.Devoir, DevoirAdmin)
