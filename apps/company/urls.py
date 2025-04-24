from rest_framework import routers

from .api import CompanyViewSet

# Create a router and register our viewset with it.
router = routers.DefaultRouter()
router.register(r"", CompanyViewSet, basename="company")

urlpatterns = []
urlpatterns += router.urls
