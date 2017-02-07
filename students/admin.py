from django.contrib import admin
from .models import (
    TestCategory,
    Test,
    Batch,
    Department,
    StudentCategory,
    Student,
    AttendanceRecord,
    TestParticipation
)

class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'roll',
        'name',
        'student_category',
        'due_date',
        'contact_number',
    )
    list_filter = (
        'due_date',
        'student_category',
        'batch',
        'is_prospective',
        'is_assistive',
    )
    search_fields = ('roll', 'name',)

    fieldsets = [
        ('Primary Info', {'fields': [
            'roll',
            'name',
            'department',
            'contact_number',
        ]}),
        ('Personal Info', {'fields': [
            'father_name',
            'mother_name',
            'blood_group',
        ]}),
        ('Admission Related Info', {'fields': [
            'admission_date',
            'expiration_date',
            'amount_total',
            'amount_paid',
            'due_date',
        ]}),
        ('Others', {'fields': [
            'is_prospective',
            'is_assistive',
            'is_problematic',
        ]}),
    ]

class AttendanceRecordAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    filter_horizontal = ('attending_students',)

class TestParticipationAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'marks')
    list_filter = ('date',)

admin.site.register(TestCategory)
admin.site.register(Test)
admin.site.register(Batch)
admin.site.register(Department)
admin.site.register(StudentCategory)
admin.site.register(Student, StudentAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)
admin.site.register(TestParticipation, TestParticipationAdmin)
