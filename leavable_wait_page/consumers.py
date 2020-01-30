from .models import AugmentedParticipant
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from importlib import import_module
import json


class LeavableWaitPageConsumer(WebsocketConsumer):
    def _get_models_module(self, app_name):
        module_name = '{}.models'.format(app_name)
        return import_module(module_name)

    def update_state(self, app_name, group_pk, index_in_pages):
        participants_on_wait_page = self._get_models_module(app_name).Player.objects.filter(
            group__pk=group_pk,
            participant__augmentedparticipant__current_wp=index_in_pages,
        )
        num_waiting_participants = len(participants_on_wait_page)
        players_per_group = self._get_models_module(app_name).Constants.players_per_group
        num_missing_participants = players_per_group - num_waiting_participants

        payload = {
            "num_waiting_participants": num_waiting_participants,
            "num_missing_participants": num_missing_participants,
        }

        async_to_sync(self.channel_layer.group_send)(
            'group_{}_{}'.format(app_name, group_pk),
            {
                "type": "group_forward",
                "text": json.dumps(payload)
            }
        )

    def connect(self):
        participant_code = self.scope['url_route']['kwargs']['participant_code']
        app_name = self.scope['url_route']['kwargs']['app_name']
        group_pk = self.scope['url_route']['kwargs']['group_pk']
        index_in_pages = self.scope['url_route']['kwargs']['index_in_pages']

        print('somebody connected from custom wp..')
        try:
            mturker = AugmentedParticipant.objects.get(Participant__code=participant_code)
        except ObjectDoesNotExist:
            return None

        mturker.current_wp = index_in_pages
        mturker.save()

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            'group_{}_{}'.format(app_name, group_pk),
            self.channel_name
        )
        self.update_state(app_name, group_pk, index_in_pages)

    # Connected to websocket.disconnect
    def disconnect(self, close_code):
        participant_code = self.scope['url_route']['kwargs']['participant_code']
        app_name = self.scope['url_route']['kwargs']['app_name']
        group_pk = self.scope['url_route']['kwargs']['group_pk']
        index_in_pages = self.scope['url_route']['kwargs']['index_in_pages']
        try:
            mturker = AugmentedParticipant.objects.get(Participant__code=participant_code)
        except ObjectDoesNotExist:
            return None

        mturker.current_wp = None
        mturker.save()
        print('somebody disconnected...')
        async_to_sync(self.channel_layer.group_discard)(
            'group_{}_{}'.format(app_name, group_pk),
            self.channel_name
        )

        self.update_state(app_name, group_pk, index_in_pages)

    # receive from room then forward to everyone in group
    def group_forward(self, event):
        self.send(text_data=event['text'])