from django.urls import path

from . import views
from .apps import App_name


app_name = App_name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category>/', views.CategoryView.as_view(), name='category'),
    path('results/', views.SearchView.as_view(), name='search'),
    path('thought/create/', views.Create.as_view(), name='create'),
    path('thought/<int:pk>/', views.Detail.as_view(), name='detail'),
    path('thought/update/<int:pk>/', views.Update.as_view(), name='update'),
    path('thought/delete/<int:pk>/', views.Delete.as_view(), name='delete'),
]
