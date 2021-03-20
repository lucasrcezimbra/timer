from time import sleep

from timer import FriendlyDuration


def test_init():
    days, hours, minutes, seconds = 12, 10, 56, 8
    duration = FriendlyDuration(days, hours, minutes, seconds)

    assert duration.days == days
    assert duration.hours == hours
    assert duration.minutes == minutes
    assert duration.seconds == seconds


class TestFromSeconds:
    def test_one_second(self):
        duration = FriendlyDuration.from_seconds(1)
        assert duration.days == 0
        assert duration.hours == 0
        assert duration.minutes == 0
        assert duration.seconds == 1

    def test_one_second_and_a_half(self):
        duration = FriendlyDuration.from_seconds(1.5)
        assert duration.days == 0
        assert duration.hours == 0
        assert duration.minutes == 0
        assert duration.seconds == 1.5

    def test_one_minute_and_one_second(self):
        seconds = FriendlyDuration.MINUTE_IN_SECONDS + 1.5

        duration = FriendlyDuration.from_seconds(seconds)

        assert duration.days == 0
        assert duration.hours == 0
        assert duration.minutes == 1
        assert duration.seconds == 1.5

    def test_one_hour_one_minute_and_one_second(self):
        seconds = (
            FriendlyDuration.HOUR_IN_SECONDS
            + FriendlyDuration.MINUTE_IN_SECONDS
            + 1.5
        )

        duration = FriendlyDuration.from_seconds(seconds)

        assert duration.days == 0
        assert duration.hours == 1
        assert duration.minutes == 1
        assert duration.seconds == 1.5

    def test_one_day_one_hour_one_minute_and_one_second(self):
        seconds = (
            FriendlyDuration.DAY_IN_SECONDS
            + FriendlyDuration.HOUR_IN_SECONDS
            + FriendlyDuration.MINUTE_IN_SECONDS
            + 1.5
        )

        duration = FriendlyDuration.from_seconds(seconds)

        assert duration.days == 1
        assert duration.hours == 1
        assert duration.minutes == 1
        assert duration.seconds == 1.5


def test_str():
    assert str(FriendlyDuration(0, 0, 0, 1)) == '1 second'
    assert str(FriendlyDuration(0, 0, 1, 0)) == '1 minute'
    assert str(FriendlyDuration(0, 1, 0, 0)) == '1 hour'
    assert str(FriendlyDuration(1, 0, 0, 0)) == '1 day'

    assert str(FriendlyDuration(0, 0, 0, 2)) == '2 seconds'
    assert str(FriendlyDuration(0, 0, 2, 0)) == '2 minutes'
    assert str(FriendlyDuration(0, 2, 0, 0)) == '2 hours'
    assert str(FriendlyDuration(2, 0, 0, 0)) == '2 days'

    assert str(FriendlyDuration(1, 1, 1, 1)) == '1 day, 1 hour, 1 minute, 1 second'


def test_timer():
    time_to_sleep, result = 1, 'x'

    @FriendlyDuration.timer
    def f(*args, **kwargs):
        sleep(time_to_sleep)
        return result

    duration, result = f()

    assert duration.seconds >= time_to_sleep
    assert result == result
