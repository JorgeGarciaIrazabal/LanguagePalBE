from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register('courses/', views.CourseView, base_name='courses')
# router.register('courses/1/students/', views.StudentView, base_name='students')

urlpatterns = [
    path('courses/<int:course_id>/students/', views.StudentsView.as_view(), name='students'),
    path('courses/<int:course_id>/students/<int:pk>', views.StudentView.as_view(), name='student'),
    path('courses/<int:course_id>/cards/', views.CardsView.as_view(), name='cards'),
    path('courses/<int:course_id>/cards/<int:pk>', views.CardView.as_view(), name='card'),
    path('courses/<int:course_id>/cards/<int:pk>/upload-translation-sound',
         views.CardView.upload_card_translation_sound, name='card-upload-translation-sound'),
    path('courses/<int:course_id>/cards/<int:pk>/upload-sentence-sound', views.CardView.upload_card_sentence_sound,
         name='card-upload-sentence-sound', ),
]
urlpatterns += router.urls
