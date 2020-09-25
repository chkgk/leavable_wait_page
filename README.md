# Leavable Wait Page for oTree

## Overview
This app implements a leavable<sup>1</sup> wait page for oTree, i.e. a wait page that gives participants the opportunity to stop waiting for other players and continue with the experiment. For example, this allows participants to continue (or quit) the experiment, if no other player is available for group matching.

A timer on the wait page indicates how much longer the participant must wait before being able to leave the study. Once the time runs out, participants can click “leave the study” (or continue waiting) and are subsequently taken to the end of the round, the app, or the study, depending on a simple setting.

The code has been tested with oTree v2.5.5 and should work with any oTree version >= 2.3.x. It is not compatible with oTree below version 2.3, as the newer versions use a different version of channels (2.x).

_Note: Although this project is heavily based on the fantastic [custom-waiting-page-for-mturk](https://github.com/chapkovski/custom-waiting-page-for-mturk), it is not a drop-in replacement!_

## Demo
A [simple demo](https://leavable-wait-page.herokuapp.com) is included with the project.

## Installation
1. Download or clone the project and copy the ``leavable_wait_page`` folder into your oTree project folder, next to your app folders. 

2. After that, add ``leavable_wait_page`` to your ``EXTENSION_APPS`` section of ``settings.py``:
```python
EXTENSION_APPS  = ['leavable_wait_page'].
```

## Usage
To include a LeavableWaitPage, just inherit your wait pages from LeavableWaitPage instead of the 'standard' oTree WaitPage:
```python
from leavable_wait_page.pages import LeavableWaitPage, SkippablePage

class MyWaitPage(LeavableWaitPage):
    ...
   
class TaskPage(SkippablePage):
    ...
```
Also inherit your other "non-wait pages" from SkippablePage instead of Page. This is necessary to allow a participant to reach the end of the module or the end of the experiment if he has waited too much.

The LeavableWaitPage is an extension of a standard oTree WaitPage with the setting ``group_by_arrival_time = True``. Consequently, it must necessarily be the first page of the page_sequence of an app.

Other standard wait pages, not located at the first position of the app, should be declared as a WaitPage, as usual.

## Settings
The LeavableWaitPage has, in addition to standard properties of an oTree WaitPage (such as ``wait_for_all_groups`` or ``group_by_arrival_time``), two additional properties:

1. ``allow_leaving_after``: After how long will the participant be offered to quit the study (in seconds). Defaults to 3600.

2. ``skip_until_the_end_of``: whether participants who ask to stop waiting should skip the whole experiment or only the current app, or only the current round. Defaults to ``experiment``. Other possible values are ``app`` and ``round``.


### Technical remarks
Leavers will go through all "is_displayed" methods but will not enter "before_next_page" of the pages that are skipped, which is the standard oTree behavior on pages that return is_displayed = False. Leavers will go through standard wait pages as a player in a one-player group.

If leavers have to go through many standard wait pages in a row,
in some cases this can create a ``redirectCycleError()``. To avoid this problem, just add an is_displayed() method to your standard wait pages and ``return False`` if the participant is detected to be a leaver.

You can detect a leaver like this:
```python
def is_displayed(self):
    """Do not show page to leavers"""
    app_name = self.player._meta.app_label
    participant = self.player.participant
    
    go_to_end_of_experiment = participant.vars.get('go_to_the_end', False)
    go_to_end_of_app = participant.vars.get('skip_the_end_of_app_{}'.format(app_name), False)
    go_to_end_of_round = participant.vars.get('skip_the_end_of_app_{}_round_{}'.format(app_name, self.round_number), False)
    
    leaver =  go_to_end_of_experiment or go_to_end_of_app or go_to_end_of_round
    return not leaver
```

## Acknowledgements
This app uses code and descriptions from the fantastic [custom-waiting-page-for-mturk](https://github.com/chapkovski/custom-waiting-page-for-mturk) by Essi Kujansuu, Nicolas Gruyer, and Philipp Chapkovski. The original license is included.

____________________________________________________
<sup>1</sup> https://en.wiktionary.org/wiki/leavable