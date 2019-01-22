from django.db.models import Max, Min
from rest_framework import generics, views
from rest_framework.response import Response

from .api.serializers import AgreementSerializer, CalendarSerializer
from .filters import AgreementFilter
from .models import Agreement, Period

# Create your views here.


class CalendarApi(views.APIView):
    def get(self, request):
        all_periods = Period.objects.all()
        # min_year = all_periods.aggregate(Min('start'))
        # max_year = all_periods.aggregate(Max('end'))
        dates = all_periods.aggregate(Min('start'), Max('end'))
        calendar = {}

        for year in range(dates['start__min'].year,
                          dates['end__max'].year + 1):
            calendar[year] = []

        for year in calendar.keys():
            for i in range(1, 13):
                i = 0
                calendar[year].append(i)

        for year in calendar.keys():
            for period in all_periods:
                if period.end.year == year:
                    calendar[year][period.end.month - 1] += 1

        mydata = [{'calendar': calendar}]
        results = CalendarSerializer(mydata, many=True).data
        return Response(results)


class AgreementApi(generics.ListAPIView):
    serializer_class = AgreementSerializer
    queryset = Agreement.objects.all()
    filter_backends = (AgreementFilter, )
