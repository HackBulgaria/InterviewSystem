from rest_framework import serializers
from .models import InterviewSlot


class InterviewSlotSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField(source='teacher_time_slot.date')

    class Meta:
        model = InterviewSlot
        fields = ('id', 'date', 'start_time')
