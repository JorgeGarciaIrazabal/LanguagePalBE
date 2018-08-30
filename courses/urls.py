from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register('courses/', views.CourseView, base_name='courses')
# router.register('courses/1/students/', views.StudentView, base_name='students')

urlpatterns = [

    path('courses/<int:course_id>/students/', views.StudentsView.as_view(), name='students'),
    path('courses/<int:course_id>/students/<int:pk>', views.StudentView.as_view(), name='students'),
]
urlpatterns += router.urls
