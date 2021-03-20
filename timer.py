import argparse
import subprocess
from time import time_ns


class FriendlyDuration:
    MICRO_IN_NANO = 1000
    MILLI_IN_NANO = MICRO_IN_NANO * 1000
    SECOND_IN_NANO = MILLI_IN_NANO * 1000
    MINUTE_IN_NANO = SECOND_IN_NANO * 60
    HOUR_IN_NANO = MINUTE_IN_NANO * 60
    DAY_IN_NANO = HOUR_IN_NANO * 24

    def __init__(self, days, hours, minutes, seconds, milli=0, micro=0, nano=0):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milli = milli
        self.micro = micro
        self.nano = nano

    @classmethod
    def timer(cls, f):
        def _f(*args, **kwargs):
            start_time = time_ns()
            result = f(*args, **kwargs)
            return cls.from_nano(time_ns() - start_time), result

        return _f

    @classmethod
    def from_nano(cls, nano):
        days, nano = divmod(nano, cls.DAY_IN_NANO)
        hours, nano = divmod(nano, cls.HOUR_IN_NANO)
        minutes, nano = divmod(nano, cls.MINUTE_IN_NANO)
        seconds, nano = divmod(nano, cls.SECOND_IN_NANO)
        milli, nano = divmod(nano, cls.MILLI_IN_NANO)
        micro, nano = divmod(nano, cls.MICRO_IN_NANO)

        return cls(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milli=milli,
            micro=micro,
            nano=nano,
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
            self._str_time_unit(self.milli, 'millisecond'),
            self._str_time_unit(self.micro, 'microsecond'),
            self._str_time_unit(self.nano, 'nanosecond'),
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
