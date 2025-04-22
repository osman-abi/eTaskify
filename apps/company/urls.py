from rest_framework import routers

from .api import CompanyCreateViewSet

# Create a router and register our viewset with it.
router = routers.DefaultRouter()
router.register(r'create', CompanyCreateViewSet, basename='company-create')

urlpatterns = [
    # Add any additional paths here if needed
]

urlpatterns += router.urls
