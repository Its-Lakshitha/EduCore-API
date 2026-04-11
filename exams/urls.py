from django.urls import path
from .views import (
    create_exam,
    list_exams,
    add_result,
    my_results,
)

urlpatterns = [
    path('create/', create_exam, name='create_exam'),
    path('', list_exams, name='list_exams'),
    path('add_result/', add_result, name='add_result'),
    path('my_results/', my_results, name='my_results'),
]