from django.db import models
from django_filters import IsoDateTimeFilter
from django_filters import rest_framework as f
from goals.models import Goal


class GoalListFilters(f.FilterSet):
    """Filter for goal list view."""

    class Meta:
        model = Goal
        fields = {
            'due_date': ('gte', 'lte'),
            'category': ('exact', 'in'),
            'status': ('exact', 'in'),
            'priority': ('exact', 'in'),
        }
    #
    filter_overrides = {
        models.DateTimeField: {'filter_class': IsoDateTimeFilter},
    }
