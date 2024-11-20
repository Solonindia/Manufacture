from django.urls import path
from . import views

urlpatterns = [
    path('', views.production_table, name='production_table'),  # Show the production table
    path('add/', views.add_data, name='add_data'),  # Add new data
]
