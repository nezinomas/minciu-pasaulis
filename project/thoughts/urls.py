from django.urls import path

from . import views
from .apps import App_name


app_name = App_name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('results/', views.SearchView.as_view(), name='search'),
    path('thought/<int:pk>/', views.Detail.as_view(), name='detail'),
]
