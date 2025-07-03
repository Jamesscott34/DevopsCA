from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = router.urls
