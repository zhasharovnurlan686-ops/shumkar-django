SHUMKAR.AI — DJANGO CMS: САЙТ + РАСШИРЕННАЯ АДМИНКА

В /admin/ доступны:
- Настройки сайта: название, главный заголовок, WhatsApp, Instagram и email.
- Услуги: добавление, редактирование, удаление, описание, значок, цена, порядок и показ/скрытие.
- Портфолио: название, категория, описание, ссылка, обложка, порядок и показ/скрытие.
- Заявки клиентов: имя, телефон, услуга, бюджет, сообщение, дата и статус обработки. Формы сайта по-прежнему открывают WhatsApp и дополнительно сохраняют заявку в Django.
- Изображения сайта: загрузка и библиотека.
- HTML-страница: полный исходный код для расширенного редактирования.

Установка в Windows PowerShell из папки с manage.py:
1. python -m venv .venv
2. .venv\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. python manage.py makemigrations sitecms
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py import_site_html
8. python manage.py runserver

Сайт: http://127.0.0.1:8000/
Админка: http://127.0.0.1:8000/admin/

Команда import_site_html не перезаписывает существующий HTML и создаёт стартовые услуги/проекты только если соответствующие таблицы пусты.
Для Render настрой DATABASE_URL на PostgreSQL и постоянное хранение MEDIA (S3/Cloudinary или persistent disk). SQLite и обычные файлы на временном диске хостинга могут пропасть после перезапуска. Установи DJANGO_SECRET_KEY через переменные окружения перед публикацией.
