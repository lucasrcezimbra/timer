from time import sleep

from timer import FriendlyDuration


def test_init():
    days, hours, minutes, seconds = 12, 10, 56, 8
    milli, micro, nano = 19, 96, 21

    duration = FriendlyDuration(
        days, hours, minutes, seconds, milli, micro, nano
    )

    assert duration.days == days
    assert duration.hours == hours
    assert duration.minutes == minutes
    assert duration.seconds == seconds
    assert duration.milli == milli
    assert duration.micro == micro
    assert duration.nano == nano


class TestFromNanoseconds:
    def test_one_nanosecond(self):
        duration = FriendlyDuration.from_nano(1)
        assert duration.days == 0
        assert duration.hours == 0
        assert duration.minutes == 0
        assert duration.seconds == 0
        assert duration.milli == 0
        assert duration.micro == 0
        assert duration.nano == 1

    def test_one_nanosecond_and_a_half(self):
        duration = FriendlyDuration.from_nano(1.5)
        assert duration.days == 0
        assert duration.hours == 0
        assert duration.minutes == 0
        assert duration.seconds == 0
        assert duration.milli == 0
        assert duration.micro == 0
        assert duration.nano == 1.5

    def test_one_all(self):
        seconds = (
            FriendlyDuration.DAY_IN_NANO
            + FriendlyDuration.HOUR_IN_NANO
            + FriendlyDuration.MINUTE_IN_NANO
            + FriendlyDuration.SECOND_IN_NANO
            + FriendlyDuration.MILLI_IN_NANO
            + FriendlyDuration.MICRO_IN_NANO
            + 1
        )

        duration = FriendlyDuration.from_nano(seconds)

        assert duration.days == 1
        assert duration.hours == 1
        assert duration.minutes == 1
        assert duration.seconds == 1
        assert duration.milli == 1
        assert duration.micro == 1
        assert duration.nano == 1


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
    assert str(FriendlyDuration(1, 1, 1, 1, 1, 1, 1)) == (
        '1 day, 1 hour, 1 minute, 1 second, 1 millisecond, 1 microsecond, 1 nanosecond'
    )
    assert str(FriendlyDuration(2, 2, 2, 2, 2, 2, 2)) == (
        '2 days, 2 hours, 2 minutes, 2 seconds, 2 milliseconds, 2 microseconds, 2 nanoseconds'
    )


def test_timer():
    time_to_sleep, result = 1, 'x'

    @FriendlyDuration.timer
    def f(*args, **kwargs):
        sleep(time_to_sleep)
        return result

    duration, result = f()

    assert duration.seconds >= time_to_sleep
    assert result == result
