from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Consulta

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'telefone', 'data_nascimento', 'genero', 'endereco')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Personalizadas', {
            'fields': ('telefone', 'data_nascimento', 'genero', 'endereco', 'fb_link', 'twitter_link', 'tiktok_link', 'instagram_link', 'bio')
        }),
    )

# Registre o modelo User
admin.site.register(User, CustomUserAdmin)

# Registre o modelo Consulta
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['raca', 'veterinario', 'doenca', 'probabilidade', 'status', 'created_at']
    search_fields = ['veterinario__username', 'doenca']
