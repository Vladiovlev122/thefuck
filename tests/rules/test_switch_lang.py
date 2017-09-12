# -*- encoding: utf-8 -*-

import pytest
from thefuck.rules import switch_lang
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command(u'фзе-пуе', 'command not found: фзе-пуе'),
    Command(u'λσ', 'command not found: λσ')])
def test_match(command):
    assert switch_lang.match(command)


@pytest.mark.parametrize('command', [
    Command(u'pat-get', 'command not found: pat-get'),
    Command(u'ls', 'command not found: ls'),
    Command(u'агсл', 'command not found: агсл'),
    Command(u'фзе-пуе', 'some info')])
def test_not_match(command):
    assert not switch_lang.match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(u'фзе-пуе штыефдд мшь', ''), 'apt-get install vim'),
    (Command(u'λσ -λα', ''), 'ls -la')])
def test_get_new_command(command, new_command):
    assert switch_lang.get_new_command(command) == new_command
