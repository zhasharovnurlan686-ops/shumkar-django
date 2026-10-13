from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils import timezone
from .models import Lead, PortfolioProject, Review, Service, SiteImage, SitePage, SiteSettings

admin.site.site_header = "Shumkar.ai"
admin.site.site_title = "Shumkar.ai Admin"
admin.site.index_title = "Панель управления студией"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "whatsapp_number", "instagram_url", "updated_at")
    fieldsets = (
        ("Бренд и главная страница", {"fields": ("site_name", "logo", "hero_title", "hero_subtitle")} ),
        ("Контакты", {"fields": ("whatsapp_number", "instagram_url", "contact_email", "contact_text")} ),
        ("SEO", {"fields": ("seo_title", "seo_description")} ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "sort_order", "is_active")
    list_editable = ("price", "sort_order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    ordering = ("sort_order", "id")
    list_per_page = 20
    actions = ("publish_selected", "hide_selected")

    @admin.action(description="Показать выбранные услуги на сайте")
    def publish_selected(self, request, queryset): queryset.update(is_active=True)

    @admin.action(description="Скрыть выбранные услуги с сайта")
    def hide_selected(self, request, queryset): queryset.update(is_active=False)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("image_thumbnail", "title", "category", "sort_order", "is_active")
    list_display_links = ("title",)
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "category", "description")
    list_filter = ("is_active", "category")
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Информация о проекте", {"fields": ("title", "category", "description", "url")} ),
        ("Изображение", {"fields": ("image", "image_preview"), "description": "Загружайте оригинал PNG, JPG или WebP. Изображение не пережимается при сохранении."}),
        ("Публикация", {"fields": ("sort_order", "is_active")} ),
    )
    ordering = ("sort_order", "id")
    list_per_page = 20
    actions = ("publish_selected", "hide_selected")

    @admin.display(description="Обложка")
    def image_thumbnail(self, obj):
        if not obj.image: return "Нет изображения"
        return format_html('<img src="{}" style="height:58px;width:100px;object-fit:contain;background:#0b1220;border-radius:8px;padding:3px;" alt="">', obj.image.url)

    @admin.display(description="Предпросмотр оригинала")
    def image_preview(self, obj):
        if not obj or not obj.image: return "Сначала сохраните проект с изображением."
        return format_html('<a href="{}" target="_blank" rel="noopener"><img src="{}" style="max-width:100%;max-height:560px;width:auto;height:auto;object-fit:contain;background:#0b1220;padding:8px;border-radius:10px;"></a><p>Нажмите на изображение, чтобы открыть оригинал в полном размере.</p>', obj.image.url, obj.image.url)

    @admin.action(description="Опубликовать выбранные проекты")
    def publish_selected(self, request, queryset): queryset.update(is_active=True)

    @admin.action(description="Скрыть выбранные проекты")
    def hide_selected(self, request, queryset): queryset.update(is_active=False)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "service", "status_badge", "created_at", "is_processed")
    list_filter = ("status", "is_processed", "created_at")
    search_fields = ("name", "phone", "service", "business", "message")
    list_editable = ("is_processed",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page = 30
    fieldsets = (
        ("Клиент", {"fields": ("name", "phone", "service", "business")} ),
        ("Запрос", {"fields": ("budget", "social", "message")} ),
        ("Обработка", {"fields": ("status", "is_processed", "created_at")} ),
    )

    @admin.display(description="Статус")
    def status_badge(self, obj):
        colors = {"new":"#2563eb", "in_progress":"#d97706", "agreed":"#0891b2", "completed":"#059669", "rejected":"#dc2626"}
        return format_html('<span style="display:inline-block;padding:4px 9px;border-radius:20px;color:white;background:{};font-size:12px;">{}</span>', colors.get(obj.status, "#64748b"), obj.get_status_display())


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "rating", "is_active", "sort_order", "created_at")
    list_editable = ("rating", "is_active", "sort_order")
    list_filter = ("is_active", "rating")
    search_fields = ("name", "role", "text")
    ordering = ("sort_order", "-created_at")
    fieldsets = (("Отзыв клиента", {"fields": ("name", "role", "text", "rating")} ), ("Публикация", {"fields": ("is_active", "sort_order")} ))


class SitePageAdminForm(forms.ModelForm):
    class Meta:
        model = SitePage
        fields = "__all__"
        widgets = {"html_content": forms.Textarea(attrs={"rows": 38, "spellcheck": "false"})}


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    form = SitePageAdminForm
    list_display = ("title", "slug", "is_published", "updated_at")
    list_editable = ("is_published",)
    search_fields = ("title", "slug")
    fieldsets = (("Страница", {"fields": ("title", "slug", "is_published")} ), ("Расширенное редактирование", {"fields": ("html_content",), "description": "Меняйте HTML только если понимаете, как устроена страница. Основной контент удобнее менять в разделах портфолио, услуг и настроек."} ))


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ("image_thumbnail", "title", "alt_text", "created_at")
    search_fields = ("title", "alt_text")
    readonly_fields = ("created_at", "image_preview")
    fields = ("title", "image", "image_preview", "alt_text", "created_at")

    @admin.display(description="Изображение")
    def image_thumbnail(self, obj):
        if not obj.image: return "Нет изображения"
        return format_html('<img src="{}" style="height:54px;width:90px;object-fit:contain;background:#0b1220;border-radius:6px;padding:3px;" alt="">', obj.image.url)

    @admin.display(description="Предпросмотр оригинала")
    def image_preview(self, obj):
        if not obj or not obj.image: return "Сначала сохраните изображение."
        return format_html('<a href="{}" target="_blank" rel="noopener"><img src="{}" style="max-width:100%;max-height:560px;width:auto;height:auto;object-fit:contain;background:#0b1220;padding:8px;border-radius:10px;"></a><p>Нажмите на изображение, чтобы открыть оригинал.</p>', obj.image.url, obj.image.url)
