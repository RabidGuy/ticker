# MIT License
#
# Copyright (c) 2019 Jack Stout
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from datetime import datetime


class Ticker:

    # 1,000,000; a one followed by six zeroes
    microseconds_per_second = 1000000

    def __init__(self, tps=1):
        self.tps = tps
        self._last_mark = 0
        self._accumulator = 0

    @property
    def tps(self):
        return self._tps

    @tps.setter
    def tps(self, ticks_per_second):
        assert int(ticks_per_second) == ticks_per_second
        assert 0 < ticks_per_second
        self._tps = ticks_per_second

    @property
    def last_mark(self):
        return self._last_mark

    @property
    def _microseconds_per_tick(self):
        return Ticker.microseconds_per_second / self.tps

    def tick(self):
        """Returns the number of unprocessed ticks.

        First call will initialize clock by setting first mark.
        This first call will return -1. All other calls will
        return an integer greater than or equal to zero.

        """
        if not self.last_mark:
            # Set firt time mark and exit.
            self._last_mark = datetime.now()
            return -1

        # Get dt, the change in time, and update mark.
        next_mark = datetime.now()
        dt = next_mark - self._last_mark
        self._last_mark = next_mark

        # Increment accumulator by change in time:
        #   1) the seconds, which are converted to microseconds.
        #   2) the microseconds, which total less than one second.
        self._accumulator += (dt.seconds * Ticker.microseconds_per_second)
        self._accumulator += dt.microseconds

        # Drain full ticks from accumulator and return count.
        ticks_elapsed = 0
        while self._accumulator >= self._microseconds_per_tick:
            self._accumulator -= self._microseconds_per_tick
            ticks_elapsed += 1
        return ticks_elapsed
