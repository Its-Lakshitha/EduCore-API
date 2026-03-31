from django.urls import path

from .views import (
    bulk_import_teachers,
    create_teacher,
    delete_teacher,
    get_teacher,
    list_teachers,
    my_teacher_profile,
    update_teacher,
)

urlpatterns = [
    path('teachers/', list_teachers),
    path('teachers/create', create_teacher),
    path('teachers/<int:id>/', get_teacher),
    path('teachers/update/<int:id>', update_teacher),
    path('teachers/delete/<int:id>', delete_teacher),
    path('teachers/me', my_teacher_profile),
    path('bulk_import/', bulk_import_teachers),
]