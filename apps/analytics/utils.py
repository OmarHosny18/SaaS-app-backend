from decimal import Decimal, ROUND_HALF_UP
from django.core.cache import cache
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from apps.jobs.models import JobApplication


def get_dashboard_data(user):
    cache_key = f"dashboard_{user.id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    base_qs = JobApplication.objects.filter(user=user)

    total_applications = base_qs.count()

    now = timezone.now()
    applications_this_month = base_qs.filter(
        applied_date__year=now.year,
        applied_date__month=now.month
    ).count()

    by_status = list(
        base_qs.values('status').annotate(count=Count('id'))
    )

    over_time = list(
        base_qs
        .annotate(month=TruncMonth('applied_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    top_titles = list(
        base_qs.values('job_title').annotate(count=Count('id')).order_by('-count')[:5]
    )

    top_locations = list(
        base_qs.values('location').annotate(count=Count('id')).order_by('-count')[:5]
    )

    def calc_rate(status_name):
        if total_applications == 0:
            return Decimal('0.00')
        count = base_qs.filter(status=status_name).count()
        return Decimal(
            str(count / total_applications * 100)
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    result = {
        'total_applications': total_applications,
        'applications_this_month': applications_this_month,
        'interview_rate': calc_rate('interview'),
        'offer_rate': calc_rate('offer'),
        'rejection_rate': calc_rate('rejected'),
        'by_status': by_status,
        'over_time': over_time,
        'top_titles': top_titles,
        'top_locations': top_locations,
    }

    cache.set(cache_key, result, timeout=60)
    return result