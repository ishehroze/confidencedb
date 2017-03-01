from django.db import models
from django.urls import reverse_lazy
from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict

MONTH_MAPPING = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}


# Required models
class TestCategory(models.Model):
    category = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return '%s' % (self.category)

    class Meta:
        verbose_name_plural = _("test categories")
        ordering = ["category"]

class Test(models.Model):
    category = models.ForeignKey(TestCategory)
    test_number = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True) # optional

    def __str__(self):
        return '%(category)s %(test_number)d' % {
            "category": self.category,
            "test_number": self.test_number,
        }

    class Meta:
        ordering = ["category", "test_number"]
        unique_together = ("category", "test_number")

class SheetCategory(models.Model):
    category = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return '%s' % (self.category)

    class Meta:
        verbose_name_plural = _("sheet categories")
        ordering = ["category"]

class Sheet(models.Model):
    category = models.ForeignKey(SheetCategory)
    sheet_number = models.SmallIntegerField()

    def __str__(self):
        return "%(category)s %(sheet_number)d" % {
            "category": self.category,
            "sheet_number": self.sheet_number
        }

    class Meta:
        ordering = ["category", "sheet_number"]
        unique_together = ("category", "sheet_number")

class Batch(models.Model):
    batch_time = models.TimeField(primary_key=True)

    def __str__(self):
        return '%s' % (self.batch_time)

    class Meta:
        verbose_name_plural = _("batches")
        ordering = ["batch_time"]

class Department(models.Model):
    department_name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return '%s' % (self.department_name)

    class Meta:
        ordering = ["department_name"]

class StudentCategory(models.Model):
    student_category_name = models.CharField(max_length=2, primary_key=True)

    def __str__(self):
        return '%s' % (self.student_category_name)

    class Meta:
        verbose_name_plural = _("student categories")
        ordering = ["student_category_name"]


# Main models
class Student(models.Model):
    BLOOD_GROUPS = (
        ('Positive (+ve)', (
                ('o+', 'O+'),
                ('a+', 'A+'),
                ('b+', 'B+'),
                ('ab+', 'AB+')
            )
        ),
        ('Negetive (-ve)', (
                ('o-', 'O-'),
                ('a-', 'A-'),
                ('b-', 'B-'),
                ('ab-', 'AB-')
            )
        )
    )

    roll = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30,
                                   blank=True,
                                   verbose_name=_("father's name")) # optional
    mother_name = models.CharField(max_length=30,
                                   blank=True,
                                   verbose_name=_("mother's name")) # optional
    blood_group = models.CharField(max_length=3,
                                   choices=BLOOD_GROUPS,
                                   blank=True) # optional
    contact_number = models.CharField(max_length=15)
    department = models.ForeignKey(Department)
    batch = models.ForeignKey(Batch)
    student_category = models.ForeignKey(StudentCategory)
    admission_date = models.DateField()
    expiration_date = models.DateField()
    amount_total = models.IntegerField()
    amount_paid = models.IntegerField()
    due_date = models.DateField()
    is_prospective = models.BooleanField(verbose_name=_("prospective"))
    is_assistive = models.BooleanField(verbose_name=_("well-wisher"))
    is_problematic = models.BooleanField(verbose_name=_("problematic"))

    def __str__(self):
        return '%(roll)s - %(name)s' % {
            "roll": self.roll,
            "name": self.name,
        }

    def get_absolute_url(self): 
        return reverse_lazy('students:details', args=[(str(self.roll))])

    def is_expired(self):
        if self.expiration_date < date.today():
            return True
        else:
            return False

    is_expired.boolean = True
    is_expired.short_description = _("expired")

    def is_payment_cleared(self):
        if self.amount_total == self.amount_paid:
            return True
        else:
            return False

    def is_overdue(self):
        if self.is_payment_cleared():
            return False
        elif self.due_date < date.today():
            return True
        else:
            return False

    def payment_status(self):
        if self.is_expired():
            return None
        elif self.is_overdue():
            return False
        elif self.is_payment_cleared():
            return True
        else:
            return None

    payment_status.boolean = True
    payment_status.short_description = _("payment status")

    def validity_days(self):
        delta = self.expiration_date - date.today()
        return delta.days if delta.days >= 0 else 0

    validity_days.short_description = _("days to expiration")

    def amount_due(self):
        return self.amount_total - self.amount_paid

    def attending_dates(self):
        return self.attendance_record_set.all().values_list('date', 
            flat=True)

    def attending_dates_breakdown(self):
        attending_dates = self.attending_dates()

        breakdown_by_months = {}

        for attending_date in attending_dates:
            month_dt = date(
                month = attending_date.month,
                year = attending_date.year,
                day = 1
            )
            
            try: 
                breakdown_by_months[month_dt].append(
                    attending_date)
            except KeyError:
                breakdown_by_months[month_dt] = \
                    [attending_date]

        return breakdown_by_months

    def test_participations_breakdown(self):
        participations = self.test_participation_set.all()
        categories = TestCategory.objects.all().values_list(
            'category', flat=True)

        participations_by_category = {
            category: participations.filter(
                    test__category=category
                ) for category in categories
        }

        return participations_by_category

    def sheets_received_breakdown(self):
        categories = SheetCategory.objects.all().values_list(
                'category', flat=True)

        sheets_by_category = {
            category: [] for category in categories
        }

        try: 
            receipts = self.received_sheets.sheets.all()
            
            for category in sheets_by_category:
                sheets_by_category[category] = \
                    receipts.filter(category=category)

            return sheets_by_category
        
        except ObjectDoesNotExist:
            return sheets_by_category

class AttendanceRecord(models.Model):
    date = models.DateField(primary_key=True, default=date.today)
    students = models.ManyToManyField(Student,
        related_name='attendance_record_set')

    def __str__(self):
        return u'Record for %s' % (self.date)

class TestParticipation(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student,
        related_name='test_participation_set')
    test = models.ForeignKey(Test,
        related_name='test_participation_set')
    marks = models.PositiveSmallIntegerField()

    def __str__(self):
        return u'%(test_category)s number %(test_number)d by %(roll)s' % {
            "test_category": self.test.category,
            "test_number": self.test.test_number,
            "roll": self.student.roll,
        }

class SheetReception(models.Model):
    student = models.OneToOneField(Student,
        related_name='received_sheets')
    sheets = models.ManyToManyField(Sheet)

    def __str__(self):
        return '%s' % (self.student)
