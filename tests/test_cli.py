import sys

import pytest

import timer
from timer import cli


def test_call_timer(mocker):
    args = ['time.py', '--', 'ls', '-la']
    mocker.patch.object(sys, 'argv', args)
    timer_spy = mocker.spy(timer, 'timer')

    cli()

    timer_spy.assert_called_once_with(args[2:])


def test_should_have_command(mocker):
    args = ['time.py']
    mocker.patch.object(sys, 'argv', args)

    with pytest.raises(SystemExit):
        cli()
