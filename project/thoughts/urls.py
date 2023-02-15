from django.urls import path

from . import views
from .apps import App_name


app_name = App_name

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category>/', views.ListView.as_view(), name='category'),
    path('results/', views.SearchView.as_view(), name='search'),
    path('thought/create/', views.CreateView.as_view(), name='create'),
    path('thought/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('thought/update/<int:pk>/', views.UpdateView.as_view(), name='update'),
    path('thought/delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
]
