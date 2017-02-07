from django.db import models

class TestCategory(models.Model):
    category = models.CharField(max_length=30, primary_key=True)
    total_tests = models.PositiveSmallIntegerField()

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
    name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    blood_group = models.CharField(max_length=3,
                                   choices=BLOOD_GROUPS)
    contact_number = models.CharField(max_length=15)
    batch = models.ForeignKey(Batch)
    student_category = models.ForeignKey(StudentCategory)
    admission_date = models.DateField()
    expiration_date = models.DateField()
    amount_total = models.IntegerField()
    amount_paid = models.IntegerField()
    # amount_due is calculated, when paid, value is 0
    due_date = models.DateField()
    is_prospective = models.BooleanField()
    is_assistive = models.BooleanField()
    is_problematic = models.BooleanField()

class AttendanceRecord(models.Model):
    date = models.DateField(primary_key=True)
    attending_students = models.ManyToManyField(Student)

class TestParticipation(models.Model):
    date = models.DateField()
    student_roll = models.ForeignKey(Student)
    test_category = models.ForeignKey(TestCategory)
    test_number = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField()
