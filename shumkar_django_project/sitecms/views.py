import json
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from bs4 import BeautifulSoup

from .models import SitePage, SiteSettings, Service, PortfolioProject, Lead


def home(request):
    # Получаем опубликованную страницу из админки.
    page = SitePage.objects.filter(
        slug='home',
        is_published=True
    ).first()

    if page:
        html = page.html_content
    else:
        template_path = Path(settings.BASE_DIR) / 'templates' / 'index.html'
        html = template_path.read_text(encoding='utf-8')

    soup = BeautifulSoup(html, 'html.parser')

    # Настройки сайта
    settings_obj = SiteSettings.objects.first()

    if settings_obj:
        if soup.title and settings_obj.site_name:
            soup.title.string = (
                f'{settings_obj.site_name} — сайты для бизнеса'
            )

        hero = soup.select_one('.hero h1, h1')
        if hero and settings_obj.hero_title:
            hero.clear()
            hero.append(settings_obj.hero_title)

        if settings_obj.whatsapp_number:
            whatsapp = 'https://wa.me/' + ''.join(
                ch for ch in settings_obj.whatsapp_number
                if ch.isdigit()
            )

            for a in soup.select('a[href*="wa.me/"]'):
                a['href'] = whatsapp

        if settings_obj.instagram_url:
            for a in soup.select('a[href*="instagram.com/"]'):
                a['href'] = settings_obj.instagram_url

    # Услуги из Django-админки
    service_grid = soup.select_one('.services-grid')
    services = Service.objects.filter(is_active=True)

    if service_grid is not None:
        service_grid.clear()

        for item in services:
            card = soup.new_tag(
                'div',
                attrs={'class': 'service-card reveal'}
            )

            inner = soup.new_tag('div')

            icon = soup.new_tag(
                'div',
                attrs={'class': 'service-icon'}
            )
            icon.string = item.icon or '◇'

            title = soup.new_tag('h3')
            title.string = item.title

            desc = soup.new_tag('p')
            desc.string = item.description

            inner.extend([icon, title, desc])

            bottom = soup.new_tag(
                'div',
                attrs={'class': 'service-bottom'}
            )
            bottom.string = (
                (item.price + ' · ') if item.price else ''
            ) + item.button_text

            card.extend([inner, bottom])
            service_grid.append(card)

    # Портфолио из Django-админки
    portfolio_grid = soup.select_one('.portfolio-grid')

    projects = PortfolioProject.objects.filter(
        is_active=True
    ).order_by('sort_order', 'id')

    if portfolio_grid is not None:
        portfolio_grid.clear()

        for index, item in enumerate(projects, 1):
            card = soup.new_tag(
                'a',
                attrs={
                    'class': 'project-card reveal',
                    'href': item.url or '#portfolio'
                }
            )

            if item.url:
                card['target'] = '_blank'
                card['rel'] = 'noopener noreferrer'

            preview = soup.new_tag(
                'div',
                attrs={'class': 'project-preview'}
            )

            # Исправленный вывод изображения портфолио
            image_url = None

            if item.image:
                try:
                    image_url = item.image.url
                except (ValueError, OSError):
                    image_url = None

            if image_url:
                img = soup.new_tag(
                    'img',
                    src=image_url,
                    alt=item.title or 'Изображение проекта',
                    loading='lazy'
                )

                img['style'] = (
                    'display:block;'
                    'width:100%;'
                    'height:100%;'
                    'min-height:200px;'
                    'object-fit:cover;'
                    'object-position:center;'
                )

                img['onerror'] = (
                    "this.style.display='none';"
                )

                preview.append(img)

            else:
                preview['style'] = (
                    'display:flex;'
                    'align-items:center;'
                    'justify-content:center;'
                    'min-height:200px;'
                    'font-size:32px;'
                    'color:#58d9ff;'
                    'background:linear-gradient('
                    '145deg,#0d1b26,#070a0e)'
                )

                preview.string = item.category or 'Проект'

            content = soup.new_tag(
                'div',
                attrs={'class': 'project-content'}
            )

            meta = soup.new_tag(
                'div',
                attrs={'class': 'project-meta'}
            )

            category = soup.new_tag('span')
            category.string = item.category or 'Проект'

            number = soup.new_tag('span')
            number.string = f'{index:02d}'

            meta.extend([category, number])

            title = soup.new_tag('h3')
            title.string = item.title

            desc = soup.new_tag('p')
            desc.string = item.description

            link = soup.new_tag(
                'span',
                attrs={'class': 'project-link'}
            )
            link.string = (
                'Открыть проект ↗' if item.url else 'Проект'
            )

            content.extend([meta, title, desc, link])
            card.extend([preview, content])
            portfolio_grid.append(card)

    # Сохраняем копию заявок в Django-админке.
    script = soup.new_tag('script')

    script.string = r"""
    (function () {
        function saveLead(data) {
            try {
                fetch('/request/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }).catch(function () {});
            } catch (e) {}
        }

        var main = document.getElementById('mainForm');

        if (main) {
            main.addEventListener('submit', function () {
                saveLead({
                    name: (document.getElementById('name') || {}).value || '',
                    phone: (document.getElementById('phone') || {}).value || '',
                    service: (document.getElementById('service') || {}).value || '',
                    business: (document.getElementById('business') || {}).value || '',
                    budget: (document.getElementById('budget') || {}).value || '',
                    social: (document.getElementById('social') || {}).value || '',
                    message: (document.getElementById('message') || {}).value || ''
                });
            });
        }

        var brief = document.getElementById('briefForm');

        if (brief) {
            brief.addEventListener('submit', function () {
                saveLead({
                    name: (document.getElementById('briefName') || {}).value || '',
                    phone: (document.getElementById('briefPhone') || {}).value || '',
                    service: (document.getElementById('briefService') || {}).value || '',
                    budget: (document.getElementById('briefBudget') || {}).value || '',
                    message: (document.getElementById('briefMessage') || {}).value || ''
                });
            });
        }
    })();
    """

    if soup.body:
        soup.body.append(script)

    return HttpResponse(str(soup))


@csrf_exempt
@require_POST
def save_lead(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        name = str(data.get('name', '')).strip()[:160]
        phone = str(data.get('phone', '')).strip()[:60]

        if not name or not phone:
            return JsonResponse(
                {
                    'ok': False,
                    'error': 'name_and_phone_required'
                },
                status=400
            )

        Lead.objects.create(
            name=name,
            phone=phone,
            service=str(data.get('service', ''))[:160],
            business=str(data.get('business', ''))[:160],
            budget=str(data.get('budget', ''))[:100],
            social=str(data.get('social', ''))[:250],
            message=str(data.get('message', ''))[:5000]
        )

        return JsonResponse({'ok': True})

    except (ValueError, TypeError, UnicodeDecodeError):
        return JsonResponse(
            {
                'ok': False,
                'error': 'invalid_json'
            },
            status=400
        )