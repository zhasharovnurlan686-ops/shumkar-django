from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from sitecms.models import SitePage, SiteSettings, Service, PortfolioProject

class Command(BaseCommand):
    help = 'Imports original Shumkar.ai HTML and creates editable CMS entries if missing.'
    def handle(self, *args, **options):
        html_path = Path(settings.BASE_DIR) / 'templates' / 'index.html'
        html = html_path.read_text(encoding='utf-8')
        page, created = SitePage.objects.get_or_create(slug='home', defaults={'title': 'Главная страница Shumkar.ai', 'html_content': html, 'is_published': True})
        self.stdout.write(self.style.SUCCESS(('Создана' if created else 'Уже существует') + f' HTML-страница: {page.title}'))
        SiteSettings.objects.get_or_create(pk=1)
        service_data = [
            ('Сайты и лендинги', 'Современные сайты для компаний, экспертов, услуг и локального бизнеса. Адаптивный дизайн и высокая скорость.', '◈'),
            ('Интернет-магазины', 'Каталог товаров, корзина, заявки, категории, админ-панель и мобильная версия.', '◫'),
            ('Telegram-боты', 'Telegram-боты для автоматизации заявок, продаж и общения с клиентами.', '◎'),
            ('UI/UX дизайн', 'Продуманный интерфейс, визуальная система бренда и структура сайта.', '◇'),
            ('Запуск проекта', 'Подключение домена, размещение сайта и передача готового проекта.', '↗'),
            ('Поддержка', 'Изменения, новые блоки, функционал и дальнейшее развитие сайта.', '∞'),
        ]
        if not Service.objects.exists():
            for i, (title, description, icon) in enumerate(service_data):
                Service.objects.create(title=title, description=description, icon=icon, sort_order=i)
        projects = [
            ('Eleganzo Mir', 'E-commerce', 'Современный интернет-магазин с каталогом товаров и мобильной адаптацией.', 'https://eleganzomir-three.vercel.app'),
            ('Речевой центр', 'Education', 'Сайт речевого центра для родителей и обучения логопедов.', 'https://logoped-two.vercel.app'),
            ('Barber Shop', 'Business', 'Сайт для барбершопа с презентацией услуг и быстрым обращением клиента.', 'https://barber-two-navy.vercel.app'),
        ]
        if not PortfolioProject.objects.exists():
            for i, (title, category, description, url) in enumerate(projects):
                PortfolioProject.objects.create(title=title, category=category, description=description, url=url, sort_order=i)
        self.stdout.write(self.style.SUCCESS('Начальные настройки, услуги и проекты добавлены при необходимости.'))
