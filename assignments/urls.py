from django.urls import path

from .views import (
    create_assignment,
    grade_submission,
    list_assignments,
    submit_assignment,
)

urlpatterns = [
    path('assignments/', list_assignments, name='list_assignments'),
    path('assignments/create/', create_assignment, name='create_assignment'),
    path('assignments/<int:assignment_id>/submit/', submit_assignment, name='submit_assignment'),
    path('assignments/<int:assignment_id>/grade/', grade_submission, name='grade_submission'),
]