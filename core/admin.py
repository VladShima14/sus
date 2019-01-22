from django.contrib import admin

from .models import Agreement, Company, Country, Period, Status


class PeriodsInLine(admin.TabularInline):
    # model = Agreement.period.through
    model = Period


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code']
    search_fields = ['name', 'iso_code']


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'status']
    search_fields = ['status']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['title', 'country']
    search_fields = ['title', 'country']


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ['company', 'negotiator', 'start_date', 'stop_date']
    search_fields = ['company__title', 'start_date', 'stop_date']
    list_filter = ('company__title',)

    inlines = [PeriodsInLine]
