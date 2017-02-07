from django.db import models

class TestCategory(models.Model):
    category = models.CharField(max_length=30, primary_key=True)
    total_tests = models.PositiveSmallIntegerField(null=False)

class Batch(models.Model):
    batch_time = models.TimeField(primary_key=True)

class Department(models.Model):
    department_name = models.CharField(max_length=30, primary_key=True)

class StudentCategory(models.Model):
    student_category_name = models.CharField(max_length=2, primary_key=True)

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
    name = models.CharField(max_length=30, null=False)
    father_name = models.CharField(max_length=30) # optional
    mother_name = models.CharField(max_length=30) # optional
    blood_group = models.CharField(max_length=3,
                                   choices=BLOOD_GROUPS)
    contact_number = models.CharField(max_length=15, null=False)
    batch = models.ForeignKey(Batch, null=False)
    student_category = models.ForeignKey(StudentCategory, null=False)
    admission_date = models.DateField(null=False)
    expiration_date = models.DateField(null=False)
    amount_total = models.IntegerField(null=False)
    amount_paid = models.IntegerField(null=False)
    # amount_due is calculated, when paid, value is 0
    due_date = models.DateField(null=False)
    is_prospective = models.BooleanField()
    is_assistive = models.BooleanField()
    is_problematic = models.BooleanField()

class AttendanceRecord(models.Model):
    date = models.DateField(primary_key=True)
    attending_students = models.ManyToManyField(Student)

class TestParticipation(models.Model):
    date = models.DateField(null=False)
    student_roll = models.ForeignKey(Student, null=False)
    test_category = models.ForeignKey(TestCategory, null=False)
    test_number = models.PositiveSmallIntegerField(null=False)
    marks = models.PositiveSmallIntegerField(null=False)
