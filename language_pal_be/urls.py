from django.urls import include, path

urlpatterns = [
    path('cards/', include('cards.urls')),
    path('', include('courses.urls')),
    path('auth/', include('lp_auth.urls')),
]
