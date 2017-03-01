from django.contrib import admin
from datetime import date
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from .models import (
    TestCategory,
    Test,
    Batch,
    Department,
    StudentCategory,
    SheetCategory,
    Sheet,
    Student,
    AttendanceRecord,
    TestParticipation,
    SheetReception
)

admin.site.site_header = 'Confidence Administration'
admin.site.site_title = 'Confidence Administration'

# Removing 'delete_selected' from admin page
admin.site.disable_action('delete_selected')

# Custom action 'make_paid' for admin change list
def make_paid(modelAdmin, request, queryset):
    for obj in queryset:
        obj.amount_paid = obj.amount_total
        obj.save()
make_paid.short_description = _("Mark selected as Paid")

# Custom Filters
class StatusFilter(admin.SimpleListFilter):
    title = _('status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('overdue', _('Overdue')),
            ('due', _('Payment Due')),
            ('paid', _('Payment Cleared')),
            ('expired', _('Expired'))
        )

    def queryset(self, request, queryset):
        today = date.today()

        if self.value() == 'overdue':
            return queryset.filter(due_date__lt=today)\
                .exclude(amount_paid=F('amount_total'))\
                .exclude(expiration_date__lt=today)

        elif self.value() == 'paid':
            return queryset.filter(amount_paid=F('amount_total'))\
                .exclude(expiration_date__lt=today)

        elif self.value() == 'expired':
            return queryset.filter(expiration_date__lt=today)

        elif self.value() == 'due':
            return queryset.filter(due_date__gte=today)\
                .exclude(amount_paid=F('amount_total'))\
                .exclude(expiration_date__lt=today)

        else:
            return queryset

class BloodGroupFilter(admin.SimpleListFilter):
    title = _('blood group')
    parameter_name = 'bldgrp'

    def lookups(self, request, model_admin):
        return (
            ('opos', _('O+')),
            ('apos', _('A+')),
            ('bpos', _('B+')),
            ('abpos', _('AB+')),
            ('oneg', _('O-')),
            ('aneg', _('A-')),
            ('bneg', _('B-')),
            ('abneg', _('AB-')),
            ('unset', _('Unassigned'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'opos':
            return queryset.filter(blood_group='o+')
        elif self.value() == 'apos':
            return queryset.filter(blood_group='a+')
        elif self.value() == 'bpos':
            return queryset.filter(blood_group='b+')
        elif self.value() == 'abpos':
            return queryset.filter(blood_group='ab+')
        elif self.value() == 'oneg':
            return queryset.filter(blood_group='o-')
        elif self.value() == 'aneg':
            return queryset.filter(blood_group='a-')
        elif self.value() == 'bneg':
            return queryset.filter(blood_group='b-')
        elif self.value() == 'abneg':
            return queryset.filter(blood_group='ab-')
        elif self.value() == 'unset':
            return queryset.exclude(blood_group__in=(
                'o+', 'a+', 'b+', 'ab+', 'o-', 'a-', 'b-', 'ab-'
            ))
        else:
            return queryset


# Model Admins and registration
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'roll',
        'name',
        'department',
        'payment_status',
        'validity_days',
        'contact_number',
    )

    list_filter = (
        StatusFilter,
        'department',
        'student_category',
        'batch',
        'admission_date',
        'is_assistive',
        BloodGroupFilter,
    )

    search_fields = ('roll', 'name',)

    fieldsets = [
        ('Admission Info', {'fields': [
            'roll',
            'name',
            'department',
            'contact_number',
            'admission_date',
            'batch',
        ]}),
        ('Personal Info', {'fields': [
            'father_name',
            'mother_name',
            'blood_group',
        ]}),
        ('Payment Info', {'fields': [
            'student_category',
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

    actions = (make_paid, 'delete_selected')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    filter_horizontal = ('students',)

@admin.register(TestParticipation)
class TestParticipationAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'marks')
    list_filter = ('date',)
    raw_id_fields = ('student', 'test')

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_filter = ('category',)

@admin.register(SheetReception)
class SheetReceptionAdmin(admin.ModelAdmin):
    raw_id_fields = ('student',)
    filter_horizontal = ('sheets',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_filter = ('category',)

admin.site.register(TestCategory)
admin.site.register(Batch)
admin.site.register(Department)
admin.site.register(StudentCategory)
admin.site.register(SheetCategory)
