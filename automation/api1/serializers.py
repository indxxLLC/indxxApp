# api/serializers.py

from rest_framework import serializers
from .models import Calendarlist
#from django.contrib.auth.models import Calendarlist


class CalendarlistSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Calendarlist
        fields = ('id', 'category', 'code', 'description')
        read_only_fields = ('date_created', 'date_modified')