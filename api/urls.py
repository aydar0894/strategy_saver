from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^save_strategy$', views.save_strategy),
    url(r'^strategies_list$', views.strategies_list),
    url(r'^get_user_strategies$', views.get_user_strategies),
    url(r'^get_bot_by_id$', views.get_bot_by_id),
    url(r'^remove_bot_by_id$', views.remove_bot_by_id),
    url(r'^get_backtester_error_codes$', views.get_backtester_error_codes),
    url(r'^add_error_code$', views.add_error_code),
    url(r'^update_by_id$', views.update_by_id),
    url(r'^published_strategies_list$', views.published_strategies_list),
    url(r'^publish_strategy$', views.publish_strategy),
    url(r'^get_user_published_strategies$', views.get_user_published_strategies)

]
