from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
# from .router import router
from companies import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^companies/', include('companies.urls')),
    # url(r'^api/', include(router.urls))
    # url(r'^stock/', views.StockList.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
