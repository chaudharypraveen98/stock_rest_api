from django.conf.urls import url, include
from django.contrib import admin

# from .router import router
from rest_api.router import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^companies/', include('companies.urls')),
    url(r'^api/', include(router.urls))
    # url(r'^stock/', views.StockList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
