# Initial schema matching the original Shumkar CMS models.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160, verbose_name='Имя')),
                ('phone', models.CharField(max_length=60, verbose_name='Телефон')),
                ('service', models.CharField(blank=True, max_length=160, verbose_name='Услуга')),
                ('business', models.CharField(blank=True, max_length=160, verbose_name='Тип бизнеса')),
                ('budget', models.CharField(blank=True, max_length=100, verbose_name='Бюджет')),
                ('social', models.CharField(blank=True, max_length=250, verbose_name='Instagram / сайт')),
                ('message', models.TextField(blank=True, verbose_name='Задача / сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Получена')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Обработана')),
            ],
            options={'verbose_name': 'Заявка клиента', 'verbose_name_plural': 'Заявки клиентов', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='PortfolioProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160, verbose_name='Название проекта')),
                ('category', models.CharField(default='Business', max_length=100, verbose_name='Категория')),
                ('description', models.TextField(verbose_name='Описание')),
                ('url', models.URLField(blank=True, verbose_name='Ссылка на проект')),
                ('image', models.ImageField(blank=True, null=True, upload_to='portfolio/%Y/%m/', verbose_name='Обложка проекта')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
            ],
            options={'verbose_name': 'Проект портфолио', 'verbose_name_plural': 'Портфолио', 'ordering': ['sort_order', 'id']},
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160, verbose_name='Название услуги')),
                ('description', models.TextField(verbose_name='Описание')),
                ('icon', models.CharField(blank=True, default='◇', max_length=20, verbose_name='Значок')),
                ('price', models.CharField(blank=True, help_text='Например: от 15 000 сом', max_length=80, verbose_name='Цена / от')),
                ('button_text', models.CharField(default='Подробнее →', max_length=80, verbose_name='Текст кнопки')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
            ],
            options={'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги', 'ordering': ['sort_order', 'id']},
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название изображения')),
                ('image', models.ImageField(upload_to='site-images/%Y/%m/', verbose_name='Файл изображения')),
                ('alt_text', models.CharField(blank=True, max_length=250, verbose_name='Описание изображения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Загружено')),
            ],
            options={'verbose_name': 'Изображение сайта', 'verbose_name_plural': 'Изображения сайта'},
        ),
        migrations.CreateModel(
            name='SitePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Главная страница', max_length=200, verbose_name='Название страницы')),
                ('slug', models.SlugField(default='home', max_length=100, unique=True, verbose_name='Адрес страницы')),
                ('html_content', models.TextField(help_text='Дополнительное редактирование исходного HTML.', verbose_name='Полный HTML-код страницы')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликована')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={'verbose_name': 'HTML-страница', 'verbose_name_plural': 'HTML-страницы'},
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Shumkar.ai', max_length=120, verbose_name='Название студии')),
                ('hero_title', models.CharField(default='Создаём сайты, которые помогают бизнесу расти', max_length=250, verbose_name='Главный заголовок')),
                ('hero_subtitle', models.TextField(default='Современные сайты и цифровые решения для бизнеса.', verbose_name='Подзаголовок на главной')),
                ('whatsapp_number', models.CharField(default='996705501570', max_length=30, verbose_name='WhatsApp номер с кодом страны, только цифры')),
                ('instagram_url', models.URLField(default='https://instagram.com/shumkar.ai', verbose_name='Ссылка Instagram')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Email для связи')),
                ('contact_text', models.CharField(default='Напишите нам, чтобы обсудить ваш проект', max_length=250, verbose_name='Текст контакта')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={'verbose_name': 'Настройки сайта', 'verbose_name_plural': 'Настройки сайта'},
        ),
    ]
