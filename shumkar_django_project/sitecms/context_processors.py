from django.utils import timezone
from .models import Lead, PortfolioProject, Review, Service


def dashboard_data(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return {}
    today = timezone.localdate()
    return {
        "shumkar_dashboard": {
            "projects_count": PortfolioProject.objects.count(),
            "services_count": Service.objects.count(),
            "leads_today": Lead.objects.filter(created_at__date=today).count(),
            "leads_month": Lead.objects.filter(created_at__year=today.year, created_at__month=today.month).count(),
            "leads_open": Lead.objects.filter(is_processed=False).count(),
            "reviews_count": Review.objects.count(),
            "recent_leads": Lead.objects.order_by("-created_at")[:6],
        }
    }
