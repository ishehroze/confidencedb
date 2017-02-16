from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.translation import ugettext_lazy as _

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
    # amount_due is calculated, when paid, value is 0
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
        return reverse('students.views.details', args=[(str(self.roll))])

    def is_overdue(self):
        if self.due_date < date.today():
            return True
        else:
            return False

    def is_expired_property(self):
        if self.expiration_date < date.today():
            return True
        else:
            return False

    is_expired_property.short_description = _("expired")
    is_expired = property(is_expired_property)

    def is_payment_cleared_property(self):
        if self.amount_total == self.amount_paid:
            return True
        else:
            return False

    is_payment_cleared_property.short_description = _("payment complete")
    is_payment_cleared = property(is_payment_cleared_property)

    class Meta:
        ordering = ["roll"]

class AttendanceRecord(models.Model):
    date = models.DateField(primary_key=True)
    attending_students = models.ManyToManyField(Student)

    def __str__(self):
        return u'Record for %s' % (self.date)

    class Meta:
        ordering = ["date"]

class TestParticipation(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student)
    test = models.ForeignKey(Test)
    marks = models.PositiveSmallIntegerField()

    def __str__(self):
        return u'%(test_category)s number %(test_number)d by %(roll)s' % {
            "test_category": self.test.category,
            "test_number": self.test.test_number,
            "roll": self.student.roll,
        }

    class Meta:
        ordering = ["student", "test"]

class SheetDistribution(models.Model):
    student = models.OneToOneField(Student)
    sheet = models.ManyToManyField(SheetCategory)

    def __str__(self):
        return '%s' % (self.student)

    class Meta:
        ordering = ["student"]
