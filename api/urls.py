from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^save_strategy$', views.save_strategy),
    url(r'^strategies_list$', views.strategies_list),
    url(r'^get_user_strategies$', views.get_user_strategies),
    url(r'^get_bot_by_id$', views.get_bot_by_id),
    url(r'^remove_bot_by_id$', views.remove_bot_by_id)
]
