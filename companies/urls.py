from django.urls import path

from . import views

app_name = 'companies'
urlpatterns = [
    # IT IS FOR JSON RESPONSE SERIALIZER
    # path('', views.stock, name='list'),
    # path('', views.StockApiView.as_view(), name='list'),
    path('', views.GenericStockView.as_view(), name='list'),
    path('<int:pk>/', views.StockApiViewDetail.as_view(), name='detail'),
    # path('<int:pk>/', views.stock_details, name='detail'),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('logout/', views.LogoutApiView.as_view(), name="logout")
]
