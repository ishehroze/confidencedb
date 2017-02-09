from django.db import models
from django.urls import reverse
from datetime import date

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

class TestCategory(models.Model):
    category = models.CharField(max_length=30, primary_key=True)
    total_tests = models.PositiveSmallIntegerField()

    def __str__(self):
        return u'%s' % (self.category)

    class Meta:
        verbose_name_plural = "test categories"

class Test(models.Model):
    category = models.ForeignKey(TestCategory)
    test_number = models.PositiveSmallIntegerField()
    test_description = models.TextField(blank=True) # optional

    def __str__(self):
        return u'%s %d' % (self.category, self.test_number)

class Batch(models.Model):
    batch_time = models.TimeField(primary_key=True)

    def __str__(self):
        return u'%s' % (self.batch_time)

    class Meta:
        verbose_name_plural = "batches"

class Department(models.Model):
    department_name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return u'%s' % (self.department_name)

class StudentCategory(models.Model):
    student_category_name = models.CharField(max_length=2, primary_key=True)

    def __str__(self):
        return u'%s' % (self.student_category_name)

    class Meta:
        verbose_name_plural = "student categories"

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
                                   verbose_name="father's name") # optional
    mother_name = models.CharField(max_length=30,
                                   blank=True,
                                   verbose_name="mother's name") # optional
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
    is_prospective = models.BooleanField(verbose_name="prospective")
    is_assistive = models.BooleanField(verbose_name="assistive")
    is_problematic = models.BooleanField(verbose_name="problematic")

    def __str__(self):
        return u'%s - %s' % (self.roll, self.name)

    def get_absolute_url(self):
        return reverse('students.views.details', args=[(str(self.roll))])

    def payment_info(self):
        if self.expiration_date < date.today():
            return "EXPIRED"
        elif self.amount_total == self.amount_paid:
            return "Paid"
        else:
            if self.due_date < date.today():
                return "OVERDUE"
            else:
                return "%s (tk. %d)" % (
                    self.due_date,
                    self.amount_total - self.amount_paid
                )

class AttendanceRecord(models.Model):
    date = models.DateField(primary_key=True)
    attending_students = models.ManyToManyField(Student)

    def __str__(self):
        return u'Record for %s' % (self.date)

    def get_absolute_url(self):
        return reverse('students.views.test_participation',
                       args=[str(self.date.day),
                             str(self.date.month),
                             str(self.date.year)])

class TestParticipation(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student)
    test = models.ForeignKey(Test)
    marks = models.PositiveSmallIntegerField()

    def __str__(self):
        return u'%s number %d by %s' % (self.test.category,
                              self.test.test_number,
                              self.student.roll)
