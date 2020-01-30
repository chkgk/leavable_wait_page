from django.conf.urls import url
from leavable_wait_page.consumers import LeavableWaitPageConsumer

websocket_routes = [
    url(r'^waiting_page/(?P<participant_code>\w+)/(?P<app_name>\w+)/(?P<group_pk>\w+)/(?P<player_pk>\w+)/(?P<index_in_pages>\w+)$', LeavableWaitPageConsumer),
]