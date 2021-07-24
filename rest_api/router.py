from rest_framework import routers

from companies.views import StockViewSet

router = routers.DefaultRouter()
router.register('companies', StockViewSet)
