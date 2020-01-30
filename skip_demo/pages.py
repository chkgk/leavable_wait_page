from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from leavable_wait_page.pages import SkippablePage, LeavableWaitPage


class GroupParticipants(LeavableWaitPage):
    """This is a wait page that allows players to quit waiting after 10 seconds."""
    allow_leaving_after = 10

class MainTask(SkippablePage):
    """This is the main task page and is skipped if participants left the wait page."""
    pass

class Results(SkippablePage):
    """This page is only shown to those who complete the task."""
    pass

class Dropouts(Page):
    """This page is only shown to those who left the wait page."""
    def is_displayed(self) -> bool:
        return self.player.participant.vars.get('go_to_the_end', False)


page_sequence = [
    GroupParticipants,
    MainTask,
    Results,
    Dropouts
]
