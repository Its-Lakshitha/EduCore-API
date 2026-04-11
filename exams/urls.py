from django.urls import path

from .views import (
    add_result,
    create_exam,
    exam_view,
    list_exams,
    my_results,
)

urlpatterns = [
    path('create/', create_exam, name='create_exam'),
    path('', list_exams, name='list_exams'),
    path('<int:exam_id>/', exam_view, name='exam_view'),
    path('add_result/', add_result, name='add_result'),
    path('my_results/', my_results, name='my_results'),
]