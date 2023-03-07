from . views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('product', ProductViewSet, basename='product')

urlpatterns = router.urls
