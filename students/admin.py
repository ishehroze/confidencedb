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

models = (
    TestCategory,
    Test,
    Batch,
    Department,
    StudentCategory,
    Student,
    AttendanceRecord,
    TestParticipation
)

for model in models:
    admin.site.register(model)
