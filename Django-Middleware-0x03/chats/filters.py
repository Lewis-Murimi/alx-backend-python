import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    user = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
