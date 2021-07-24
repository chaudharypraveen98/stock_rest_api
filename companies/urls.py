from django.urls import path

from . import views

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

"""
This router is similar to SimpleRouter as above, but additionally includes a default API root view, that returns a 
response containing hyperlinks to all the list views. It also generates routes for optional .json style format 
suffixes. 
"""
app_name = 'companies'
urlpatterns = [
    # IT IS FOR JSON RESPONSE SERIALIZER
    # path('', views.stock, name='list'),
    # path('', views.StockApiView.as_view(), name='list'),
    path('', views.GenericStockView.as_view(), name='list'),
    path('<int:pk>/', views.GenericStockView.as_view(), name='detail'),
    # path('<int:pk>/', views.stock_details, name='detail'),
    path('login/', views.LoginApiView.as_view(), name="login"),
    # path('jwttoken/', TokenObtainPairView.as_view(), name="access"),
    # path('jwttoken/refresh', TokenRefreshView.as_view(), name="refresh")
]
