from django.urls import path
from .views import TrackingPerSalesStaff

urlpatterns = [
    path('tracking_per_sales_staff/', TrackingPerSalesStaff.as_view(), \
         name='tracking_per_sales_staff')
]
