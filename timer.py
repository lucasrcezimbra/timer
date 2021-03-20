import argparse
import subprocess
from time import time


class FriendlyDuration:
    MINUTE_IN_SECONDS = 60
    HOUR_IN_SECONDS = MINUTE_IN_SECONDS * 60
    DAY_IN_SECONDS = HOUR_IN_SECONDS * 24

    def __init__(self, days, hours, minutes, seconds):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @classmethod
    def timer(cls, f):
        def _f(*args, **kwargs):
            start_time = time()
            result = f(*args, **kwargs)
            return cls.from_seconds(time() - start_time), result
        return _f

    @classmethod
    def from_seconds(cls, seconds):
        days, seconds = divmod(seconds, cls.DAY_IN_SECONDS)
        hours, seconds = divmod(seconds, cls.HOUR_IN_SECONDS)
        minutes, seconds = divmod(seconds, cls.MINUTE_IN_SECONDS)
        return cls(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
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

    print(timer(args.command))


if __name__ == '__main__':
    cli()
