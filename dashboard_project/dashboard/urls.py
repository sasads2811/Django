from django.urls import path
from . import views

urlpatterns = [
    path('monthly-averages/', views.monthly_averages_view, name='monthly_averages'),
    path('monthly-averages/bpy', views.monthly_averages_view_by_year_and_province, name='monthly_averages_by_year_and_province'),
    path('total_monthly_scores/', views.total_monthly_scores, name='total_monthly_scores'),
    path('highest_score_of_the_month/', views.highest_score_of_the_month, name='highest_score_of_the_month'),
    # Add paths for other reports
]
