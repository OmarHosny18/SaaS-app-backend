import django_filters
from .models import JobApplication


class JobApplicationFilter(django_filters.FilterSet):

    status = django_filters.ChoiceFilter(
        choices=JobApplication.STATUS_CHOICES
    )

    tags = django_filters.CharFilter(
        field_name='tags__name',
        lookup_expr='iexact'
    )

    applied_date_after = django_filters.DateFilter(
        field_name='applied_date',
        lookup_expr='gte'
    )

    applied_date_before = django_filters.DateFilter(
        field_name='applied_date',
        lookup_expr='lte'
    )

    class Meta:
        model = JobApplication
        fields = ['status', 'tags', 'applied_date_after', 'applied_date_before']