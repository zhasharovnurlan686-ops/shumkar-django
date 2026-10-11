from django.db import models

class SitePage(models.Model):
    title = models.CharField('Название страницы', max_length=200, default='Главная страница')
    slug = models.SlugField('Адрес страницы', max_length=100, unique=True, default='home')
    html_content = models.TextField('Полный HTML-код страницы', help_text='Дополнительное редактирование исходного HTML.')
    is_published = models.BooleanField('Опубликована', default=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    class Meta:
        verbose_name = 'HTML-страница'; verbose_name_plural = 'HTML-страницы'
    def __str__(self): return self.title

class SiteSettings(models.Model):
    site_name = models.CharField('Название студии', max_length=120, default='Shumkar.ai')
    hero_title = models.CharField('Главный заголовок', max_length=250, default='Создаём сайты, которые помогают бизнесу расти')
    hero_subtitle = models.TextField('Подзаголовок на главной', default='Современные сайты и цифровые решения для бизнеса.')
    whatsapp_number = models.CharField('WhatsApp номер с кодом страны, только цифры', max_length=30, default='996705501570')
    instagram_url = models.URLField('Ссылка Instagram', default='https://instagram.com/shumkar.ai')
    contact_email = models.EmailField('Email для связи', blank=True)
    contact_text = models.CharField('Текст контакта', max_length=250, default='Напишите нам, чтобы обсудить ваш проект')
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    class Meta:
        verbose_name = 'Настройки сайта'; verbose_name_plural = 'Настройки сайта'
    def __str__(self): return self.site_name

class Service(models.Model):
    title = models.CharField('Название услуги', max_length=160)
    description = models.TextField('Описание')
    icon = models.CharField('Значок', max_length=20, default='◇', blank=True)
    price = models.CharField('Цена / от', max_length=80, blank=True, help_text='Например: от 15 000 сом')
    button_text = models.CharField('Текст кнопки', max_length=80, default='Подробнее →')
    sort_order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    class Meta:
        ordering = ['sort_order', 'id']; verbose_name = 'Услуга'; verbose_name_plural = 'Услуги'
    def __str__(self): return self.title

class PortfolioProject(models.Model):
    title = models.CharField('Название проекта', max_length=160)
    category = models.CharField('Категория', max_length=100, default='Business')
    description = models.TextField('Описание')
    url = models.URLField('Ссылка на проект', blank=True)
    image = models.ImageField('Обложка проекта', upload_to='portfolio/%Y/%m/', blank=True, null=True)
    sort_order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    class Meta:
        ordering = ['sort_order', 'id']; verbose_name = 'Проект портфолио'; verbose_name_plural = 'Портфолио'
    def __str__(self): return self.title

class Lead(models.Model):
    name = models.CharField('Имя', max_length=160)
    phone = models.CharField('Телефон', max_length=60)
    service = models.CharField('Услуга', max_length=160, blank=True)
    business = models.CharField('Тип бизнеса', max_length=160, blank=True)
    budget = models.CharField('Бюджет', max_length=100, blank=True)
    social = models.CharField('Instagram / сайт', max_length=250, blank=True)
    message = models.TextField('Задача / сообщение', blank=True)
    created_at = models.DateTimeField('Получена', auto_now_add=True)
    is_processed = models.BooleanField('Обработана', default=False)
    class Meta:
        ordering = ['-created_at']; verbose_name = 'Заявка клиента'; verbose_name_plural = 'Заявки клиентов'
    def __str__(self): return f'{self.name} — {self.phone}'

class SiteImage(models.Model):
    title = models.CharField('Название изображения', max_length=200)
    image = models.ImageField('Файл изображения', upload_to='site-images/%Y/%m/')
    alt_text = models.CharField('Описание изображения', max_length=250, blank=True)
    created_at = models.DateTimeField('Загружено', auto_now_add=True)
    class Meta:
        verbose_name = 'Изображение сайта'; verbose_name_plural = 'Изображения сайта'
    def __str__(self): return self.title
