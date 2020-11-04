from django.urls import path
from courses.api import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('validate/<id>/', views.validate, name='validate'),
    path('submit-coupon/<course_url_base64>/', views.submit_coupon, name='submit-coupon'),

]