from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("sitecms.urls")),
]

# Раздача загруженных изображений.
# Для Render production используйте постоянный диск или облачное хранилище,
# иначе файлы на локальном диске могут пропасть после перезапуска.
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
