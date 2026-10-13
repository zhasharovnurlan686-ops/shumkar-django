import json
import logging
from pathlib import Path

from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    Lead,
    PortfolioProject,
    Review,
    Service,
    SitePage,
    SiteSettings,
)

logger = logging.getLogger(__name__)


def home(request):
    try:
        return _render_home(request)
    except Exception:
        logger.exception("SHUMKAR HOME PAGE ERROR")
        return HttpResponse(
            "Ошибка загрузки главной страницы. "
            "Подробности сохранены в логах сервера.",
            status=500,
            content_type="text/plain; charset=utf-8",
        )


def _render_home(request):
    page = SitePage.objects.filter(
        slug="home",
        is_published=True,
    ).first()

    if page:
        html = page.html_content
    else:
        template_path = Path(settings.BASE_DIR) / "templates" / "index.html"
        html = template_path.read_text(encoding="utf-8")

    settings_obj = SiteSettings.objects.first()
    soup = BeautifulSoup(html, "html.parser")

    if settings_obj:
        if soup.title:
            soup.title.string = (
                settings_obj.seo_title
                or f"{settings_obj.site_name} — сайты для бизнеса"
            )

        if settings_obj.seo_description:
            meta_description = soup.find(
                "meta",
                attrs={"name": "description"},
            )

            if meta_description is None and soup.head:
                meta_description = soup.new_tag(
                    "meta",
                    attrs={
                        "name": "description",
                        "content": settings_obj.seo_description,
                    },
                )
                soup.head.append(meta_description)
            elif meta_description is not None:
                meta_description["content"] = settings_obj.seo_description

        hero = soup.select_one(".hero h1, h1")
        if hero and settings_obj.hero_title:
            hero.clear()
            hero.append(settings_obj.hero_title)

        hero_subtitle = soup.select_one(".hero-description")
        if hero_subtitle and settings_obj.hero_subtitle:
            hero_subtitle.clear()
            hero_subtitle.append(settings_obj.hero_subtitle)

        if settings_obj.logo:
            logo_mark = soup.select_one(".logo .logo-mark")

            if logo_mark:
                logo_mark.clear()
                logo_img = soup.new_tag(
                    "img",
                    src=settings_obj.logo.url,
                    alt=settings_obj.site_name,
                    style=(
                        "display:block;width:100%;height:100%;"
                        "object-fit:contain;"
                    ),
                )
                logo_mark.append(logo_img)

        whatsapp_number = "".join(
            char
            for char in (settings_obj.whatsapp_number or "")
            if char.isdigit()
        )

        if whatsapp_number:
            whatsapp = f"https://wa.me/{whatsapp_number}"

            for link in soup.select('a[href*="wa.me/"]'):
                link["href"] = whatsapp

        if settings_obj.instagram_url:
            for link in soup.select('a[href*="instagram.com/"]'):
                link["href"] = settings_obj.instagram_url

    service_grid = soup.select_one(".services-grid")
    services = list(Service.objects.filter(is_active=True))

    if service_grid is not None:
        service_grid.clear()

        for item in services:
            card = soup.new_tag(
                "div",
                attrs={"class": "service-card reveal"},
            )

            inner = soup.new_tag("div")

            icon = soup.new_tag(
                "div",
                attrs={"class": "service-icon"},
            )
            icon.string = item.icon or "◇"

            title = soup.new_tag("h3")
            title.string = item.title

            description = soup.new_tag("p")
            description.string = item.description

            inner.extend([icon, title, description])

            bottom = soup.new_tag(
                "div",
                attrs={"class": "service-bottom"},
            )
            bottom.string = (
                (item.price + " · ") if item.price else ""
            ) + item.button_text

            card.extend([inner, bottom])
            service_grid.append(card)

    portfolio_grid = soup.select_one(".portfolio-grid")
    projects = list(
        PortfolioProject.objects.filter(is_active=True)
    )

    if portfolio_grid is not None:
        portfolio_grid.clear()

        for index, item in enumerate(projects, 1):
            card = soup.new_tag(
                "a",
                attrs={
                    "class": "project-card reveal",
                    "href": item.url or "#portfolio",
                },
            )

            if item.url:
                card["target"] = "_blank"
                card["rel"] = "noopener noreferrer"

            preview = soup.new_tag(
                "div",
                attrs={"class": "project-preview"},
            )

            if item.image:
                image = soup.new_tag(
                    "img",
                    src=item.image.url,
                    alt=item.title,
                    loading="lazy",
                    decoding="async",
                    style=(
                        "display:block;width:100%;height:100%;"
                        "object-fit:contain;object-position:center;"
                        "image-rendering:auto;background:#070a0e;"
                    ),
                )
                preview.append(image)
            else:
                preview["style"] = (
                    "display:flex;align-items:center;"
                    "justify-content:center;font-size:32px;"
                    "color:#58d9ff;"
                    "background:linear-gradient(145deg,#0d1b26,#070a0e)"
                )
                preview.string = item.category or "Проект"

            content = soup.new_tag(
                "div",
                attrs={"class": "project-content"},
            )

            meta = soup.new_tag(
                "div",
                attrs={"class": "project-meta"},
            )

            category = soup.new_tag("span")
            category.string = item.category or ""

            number = soup.new_tag("span")
            number.string = f"{index:02d}"

            meta.extend([category, number])

            title = soup.new_tag("h3")
            title.string = item.title

            description = soup.new_tag("p")
            description.string = item.description

            project_link = soup.new_tag(
                "span",
                attrs={"class": "project-link"},
            )
            project_link.string = (
                "Открыть проект ↗" if item.url else "Проект"
            )

            content.extend(
                [meta, title, description, project_link]
            )
            card.extend([preview, content])
            portfolio_grid.append(card)

    testimonial_grid = soup.select_one(".testimonials")
    reviews = list(Review.objects.filter(is_active=True))

    if testimonial_grid is not None:
        testimonial_grid.clear()

        if not reviews:
            testimonial_section = testimonial_grid.find_parent("section")

            if testimonial_section:
                testimonial_section.decompose()

        else:
            for review in reviews:
                card = soup.new_tag(
                    "div",
                    attrs={"class": "testimonial reveal"},
                )

                stars = soup.new_tag(
                    "div",
                    attrs={"class": "stars"},
                )
                stars.string = "★" * max(1, min(5, review.rating))

                quote = soup.new_tag("p")
                quote.string = f"«{review.text}»"

                author = soup.new_tag(
                    "div",
                    attrs={"class": "author"},
                )

                avatar = soup.new_tag(
                    "div",
                    attrs={"class": "author-avatar"},
                )
                avatar.string = (review.name[:1] or "К").upper()

                author_details = soup.new_tag("div")

                name = soup.new_tag("strong")
                name.string = review.name

                role = soup.new_tag("span")
                role.string = review.role or ""

                author_details.extend([name, role])
                author.extend([avatar, author_details])
                card.extend([stars, quote, author])

                testimonial_grid.append(card)

    script = soup.new_tag("script")
    script.string = r"""(function(){
      function saveLead(data){
        try {
          fetch('/request/', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(data)
          }).catch(function(){});
        } catch(e) {}
      }

      var main=document.getElementById('mainForm');
      if(main) main.addEventListener('submit',function(){
        saveLead({
          name:(document.getElementById('name')||{}).value||'',
          phone:(document.getElementById('phone')||{}).value||'',
          service:(document.getElementById('service')||{}).value||'',
          business:(document.getElementById('business')||{}).value||'',
          budget:(document.getElementById('budget')||{}).value||'',
          social:(document.getElementById('social')||{}).value||'',
          message:(document.getElementById('message')||{}).value||''
        });
      });

      var brief=document.getElementById('briefForm');
      if(brief) brief.addEventListener('submit',function(){
        saveLead({
          name:(document.getElementById('briefName')||{}).value||'',
          phone:(document.getElementById('briefPhone')||{}).value||'',
          service:(document.getElementById('briefService')||{}).value||'',
          budget:(document.getElementById('briefBudget')||{}).value||'',
          message:(document.getElementById('briefMessage')||{}).value||''
        });
      });
    })();"""

    if soup.body:
        soup.body.append(script)

    return HttpResponse(str(soup))


@csrf_exempt
@require_POST
def save_lead(request):
    try:
        data = json.loads(request.body.decode("utf-8"))

        name = str(data.get("name", "")).strip()[:160]
        phone = str(data.get("phone", "")).strip()[:60]

        if not name or not phone:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "name_and_phone_required",
                },
                status=400,
            )

        Lead.objects.create(
            name=name,
            phone=phone,
            service=str(data.get("service", ""))[:160],
            business=str(data.get("business", ""))[:160],
            budget=str(data.get("budget", ""))[:100],
            social=str(data.get("social", ""))[:250],
            message=str(data.get("message", ""))[:5000],
        )

        return JsonResponse({"ok": True})

    except (ValueError, TypeError, UnicodeDecodeError):
        return JsonResponse(
            {"ok": False, "error": "invalid_json"},
            status=400,
        )
