from timer import FriendlyDuration, timer


def test_timer(mocker):
    subprocess_mock = mocker.patch('timer.subprocess', autospec=True)
    subprocess_args = ['ls', '-la']

    duration, _ = timer(subprocess_args)

    subprocess_mock.run.assert_called_once_with(subprocess_args)
    assert isinstance(duration, FriendlyDuration)
