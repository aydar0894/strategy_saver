from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^save_strategy$', views.save_strategy)
]
