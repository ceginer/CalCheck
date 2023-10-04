from django.urls import path

from . import views

app_name = 'calcheck'

urlpatterns = [
    path('', views.ImageUpload.as_view(), name='upload_img'),
    path('check/<int:id>', views.CheckCalories.as_view(), name='check_calories'),
]
