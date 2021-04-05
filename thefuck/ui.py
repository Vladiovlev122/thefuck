# -*- encoding: utf-8 -*-

import sys
from .conf import settings
from .exceptions import NoRuleMatched
from .system import get_key
from .utils import get_alias
from . import logs, const
from .types import CorrectedCommand


def read_actions():
    """Yields actions for pressed keys."""
    while True:
        key = get_key()

        # Handle arrows, j/k (qwerty), and n/e (colemak)
        if key in (const.KEY_UP, const.KEY_CTRL_N, "k", "e"):
            yield const.ACTION_PREVIOUS
        elif key in (const.KEY_DOWN, const.KEY_CTRL_P, "j", "n"):
            yield const.ACTION_NEXT
        elif key in (const.KEY_CTRL_C, "q"):
            yield const.ACTION_ABORT
        elif key in ("\n", "\r"):
            yield const.ACTION_SELECT


class CommandSelector(object):
    """Helper for selecting rule from rules list."""

    def __init__(self, commands):
        """:type commands: Iterable[thefuck.types.CorrectedCommand]"""
        self._commands_gen = commands
        try:
            self._commands = [next(self._commands_gen)]
        except StopIteration:
            raise NoRuleMatched
        self._realised = False
        self._index = 0

    def _realise(self):
        if not self._realised:
            self._commands += list(self._commands_gen)
            self._realised = True

    def next(self):
        self._realise()
        self._index = (self._index + 1) % len(self._commands)

    def previous(self):
        self._realise()
        self._index = (self._index - 1) % len(self._commands)

    @property
    def value(self):
        """:rtype thefuck.types.CorrectedCommand"""
        return self._commands[self._index]


def select_command(corrected_commands):
    """Returns:
     - the first command when confirmation disabled;
     - None when ctrl+c pressed;
     - selected command.
    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
    :rtype: thefuck.types.CorrectedCommand | None
    """
    try:
        selector = CommandSelector(corrected_commands)
    except NoRuleMatched:
        logs.failed("No fucks given" if get_alias() == "fuck" else "Nothing found")
        return

    if not settings.require_confirmation:
        logs.show_corrected_command(selector.value)
        return selector.value

    logs.confirm_text(selector.value)

    for action in read_actions():
        if action == const.ACTION_SELECT:
            sys.stderr.write("\n")
            return selector.value
        elif action == const.ACTION_ABORT:
            logs.failed("\nAborted")
            return
        elif action == const.ACTION_PREVIOUS:
            selector.previous()
            logs.confirm_text(selector.value)
        elif action == const.ACTION_NEXT:
            selector.next()
            logs.confirm_text(selector.value)


def confirm_command(confirmation_text):
    """Returns:
     - the first command when confirmation disabled;
     - None when ctrl+c pressed;
     - selected command.
    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
    :rtype: thefuck.types.CorrectedCommand | None
    """

    logs.confirm_text(CorrectedCommand(confirmation_text, None, 0))

    for action in read_actions():
        if action == const.ACTION_SELECT:
            logs.confirmation(True)
            return True
        elif action == const.ACTION_ABORT:
            logs.confirmation(False)
            return False
