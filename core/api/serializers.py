from rest_framework import serializers

from core.models import Agreement, Period


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = ['start', 'end', 'status']


class AgreementSerializer(serializers.ModelSerializer):

    periods = PeriodSerializer(read_only=True, many=True)

    class Meta:
        model = Agreement
        fields = ['start_date', 'stop_date', 'company', 'negotiator', 'periods']


class CalendarSerializer(serializers.Serializer):
    calendar = serializers.ReadOnlyField()
