from django.contrib import admin
from django import forms
from .models import SitePage, SiteImage, SiteSettings, Service, PortfolioProject, Lead

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'whatsapp_number', 'instagram_url', 'updated_at')
    fieldsets = (('Основное', {'fields': ('site_name', 'hero_title', 'hero_subtitle')}), ('Контакты', {'fields': ('whatsapp_number', 'instagram_url', 'contact_email', 'contact_text')}))
    def has_add_permission(self, request): return not SiteSettings.objects.exists()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('title', 'category', 'description')
    list_filter = ('is_active', 'category')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone', 'service', 'message')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)

class SitePageAdminForm(forms.ModelForm):
    class Meta:
        model = SitePage
        fields = '__all__'
        widgets = {'html_content': forms.Textarea(attrs={'rows': 45, 'cols': 140, 'spellcheck': 'false'})}
@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    form = SitePageAdminForm
    list_display = ('title', 'slug', 'is_published', 'updated_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'slug', 'html_content')
    fieldsets = ((None, {'fields': ('title', 'slug', 'is_published')}), ('Исходный HTML-код (расширенное редактирование)', {'fields': ('html_content',)}))

@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_at')
    search_fields = ('title', 'alt_text')
    readonly_fields = ('created_at',)
