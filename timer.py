import argparse
import subprocess
from time import time_ns


class FriendlyDuration:
    MICROSECOND_IN_NANOSECONDS = 1000
    MILlISECOND_IN_NANOSECONDS = MICROSECOND_IN_NANOSECONDS * 1000
    SECOND_IN_NANOSECONDS = MILlISECOND_IN_NANOSECONDS * 1000
    MINUTE_IN_NANOSECONDS = SECOND_IN_NANOSECONDS * 60
    HOUR_IN_NANOSECONDS = MINUTE_IN_NANOSECONDS * 60
    DAY_IN_NANOSECONDS = HOUR_IN_NANOSECONDS * 24

    def __init__(
        self,
        days,
        hours,
        minutes,
        seconds,
        milliseconds=0,
        microseconds=0,
        nanoseconds=0,
    ):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds
        self.microseconds = microseconds
        self.nanoseconds = nanoseconds

    @classmethod
    def timer(cls, f):
        def _f(*args, **kwargs):
            start_time = time_ns()
            result = f(*args, **kwargs)
            return cls.from_nanoseconds(time_ns() - start_time), result

        return _f

    @classmethod
    def from_nanoseconds(cls, nanoseconds):
        days, nanoseconds = divmod(nanoseconds, cls.DAY_IN_NANOSECONDS)
        hours, nanoseconds = divmod(nanoseconds, cls.HOUR_IN_NANOSECONDS)
        minutes, nanoseconds = divmod(nanoseconds, cls.MINUTE_IN_NANOSECONDS)
        seconds, nanoseconds = divmod(nanoseconds, cls.SECOND_IN_NANOSECONDS)
        milliseconds, nanoseconds = divmod(nanoseconds, cls.MILlISECOND_IN_NANOSECONDS)
        microseconds, nanoseconds = divmod(nanoseconds, cls.MICROSECOND_IN_NANOSECONDS)

        return cls(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
            nanoseconds=nanoseconds,
        )

    @staticmethod
    def _str_time_unit(value, name):
        if value != 1:
            name += 's'

        return f'{value} {name}' if value else ''

    def __str__(self):
        durations = [
            self._str_time_unit(self.days, 'day'),
            self._str_time_unit(self.hours, 'hour'),
            self._str_time_unit(self.minutes, 'minute'),
            self._str_time_unit(self.seconds, 'second'),
            self._str_time_unit(self.milliseconds, 'millisecond'),
            self._str_time_unit(self.microseconds, 'microsecond'),
            self._str_time_unit(self.nanoseconds, 'nanosecond'),
        ]
        return ', '.join(d for d in durations if d)


@FriendlyDuration.timer
def timer(subprocess_args):
    subprocess.run(subprocess_args)


def cli():
    parser = argparse.ArgumentParser(
        prog='python timer.py',
        usage='%(prog)s [-h] -- [command ...]',
        description='run programs and returns the time spent in a friendly format',
    )
    parser.add_argument(
        'command',
        nargs='+',
        help='command that will have the time counted',
    )

    args = parser.parse_args()

    duration, _ = timer(args.command)
    print(duration)


if __name__ == '__main__':
    cli()
