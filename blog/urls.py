from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list, name = 'pos_list')
]