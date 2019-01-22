from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Country(models.Model):
    iso_code = models.CharField(max_length=3)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Company(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    country = models.ForeignKey(
        to='Country',
        related_name='company',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Period(models.Model):
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    status = models.ForeignKey(
        to='Status',
        related_name='status',
        on_delete=models.CASCADE
    )
    agreement = models.ForeignKey(
        to='Agreement',
        related_name='periods',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return 'Start: {}; End: {}; Status: {}'.format(
            self.start,
            self.end,
            self.status.title
        )

    def clean(self):
        if not self.pk:
            agr_start = self.agreement.start_date
            agr_end = self.agreement.stop_date

            if self.start > self.end:
                raise ValidationError(
                    'You can\'t create period where start date '
                    'more than end date'
                )

            if self.start < agr_start:
                raise ValidationError(
                    'Period\'s start date cant be '
                    'lower then agreement\'s start date'
                )

            if self.end > agr_end:
                raise ValidationError(
                    'Period\'s end date cant be '
                    'lower then agreement\'s stop date'
                )

            if self.pk not in self.agreement.periods.all():
                for period in self.agreement.periods.all():
                    if period.end >= self.start >= period.start \
                            and period.end >= self.end >= period.start:
                        raise ValidationError(
                            'You can\'t create this period,'
                            ' because inside agreement periods '
                            'should not intersect.'
                        )
        return self.pk


class Status(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'new'),
        ('ACTIVE', 'active'),
        ('RECONCILIATION', 'reconciliation'),
        ('CLOSED', 'close'),
    )

    title = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    def __str__(self):
        return self.title


class Agreement(models.Model):
    start_date = models.DateField(blank=False)
    stop_date = models.DateField(blank=False)
    company = models.ForeignKey(
        to='Company',
        related_name='company',
        on_delete=models.CASCADE
    )
    negotiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    debit = models.IntegerField()
    credit = models.IntegerField()

    def __str__(self):
        return self.company.title

    def clean(self):
        if self.start_date > self.stop_date:
            raise ValidationError(
                'You can\'t create agreement where start date '
                'more than end date'
            )
        return self.pk
