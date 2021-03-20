import sys

import pytest

import timer
from timer import FriendlyDuration, cli


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


def test_print_duration(capsys, mocker):
    args = ['time.py', '--', 'ls', '-la']
    mocker.patch.object(sys, 'argv', args)

    cli()

    captured = capsys.readouterr()
    assert 'seconds' in captured.out


def test_print_duration_time(capsys, mocker):
    args = ['time.py', '--', 'ls', '-la']
    mocker.patch.object(sys, 'argv', args)
    duration = FriendlyDuration(1, 2, 3, 4, 5, 6, 7)
    mocker.patch('timer.timer').return_value = (duration, None)

    cli()

    captured = capsys.readouterr()
    assert str(duration) in captured.out
