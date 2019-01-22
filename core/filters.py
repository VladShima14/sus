from rest_framework import filters


class AgreementFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        negotiator_ids = request.query_params.get('negotiator')
        company_ids = request.query_params.get('company')
        country_ids = request.query_params.get('country')

        if negotiator_ids:
            negotiator_ids = negotiator_ids.split(',')
            queryset = queryset.filter(negotiator_id__in=negotiator_ids)
        if company_ids:
            company_ids = company_ids.split(',')
            queryset = queryset.filter(company_id__in=company_ids)
        if country_ids:
            country_ids = country_ids.split(',')
            queryset = queryset.filter(company__country_id__in=country_ids)

        return queryset
