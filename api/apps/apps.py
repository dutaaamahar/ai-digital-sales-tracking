import os
import joblib
from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'

    tracking_per_sales_staff_model_path = os.path.join(os.path.dirname(__file__), 'models', \
                                                       'omp_model_v01_181223.joblib')
    tracking_per_sales_staff_model = joblib.load(tracking_per_sales_staff_model_path)
