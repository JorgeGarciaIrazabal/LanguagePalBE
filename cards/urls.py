from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register('', views.ViewCards, base_name='cards')

urlpatterns = router.urls
