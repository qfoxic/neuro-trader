from lib.currency.streams import (
    EnumeratedCandlesStream, EnumeratedMurrayLevelsStream,
    ReversedEnumeratedCandlesStream
)
from abc import ABC, abstractmethod
from lib.currency.utils import get_murray_level


class Move(ABC):
    def __init__(self, *levels):
        self.levels = levels
        self.next = None
        self.prev = None

    def __or__(self, other):
        self.next = other
        other.prev = self
        return other

    def root(self):
        node = self.prev
        while node:
            if not node.prev:
                return node
            node = node.prev

    @abstractmethod
    def enter(self, mlevel):
        pass

    @abstractmethod
    def exit(self, mlevel):
        pass


class Down(Move):
    def enter(self, mlevel):
        return max(self.levels) > mlevel >= min(self.levels)

    def exit(self, mlevel):
        return mlevel > max(self.levels) or mlevel < min(self.levels)


class Up(Move):
    def enter(self, mlevel):
        return min(self.levels) < mlevel <= max(self.levels)

    def exit(self, mlevel):
        return mlevel < min(self.levels) or mlevel > max(self.levels)


class Stop(Move):
    def enter(self, mlevel):
        return True

    def exit(self, mlevel):
        return True


class MurrayLevelsBaseFlow:
    initial = None

    def __init__(self, total_samples, from_pos, mrl):
        self.state = self.initial.root()
        self.murray_levels = mrl
        self.stream = iter(ReversedEnumeratedCandlesStream(total_samples, from_pos))

    def move(self):
        pos, p = next(self.stream)
        lvl = get_murray_level(self.murray_levels, p.close)
        #print(f'Level {lvl} pos {pos}')
        next_state = None
        if self.state.next is None:
            #print(f'End {self.state}')
            self.state = self.initial
            return 2
        if self.state.enter(lvl):
            #print(f'Entered {self.state}')
            next_state = self.state.next
        if self.state.exit(lvl):
            #print(f'Exit {self.state}')
            return 3
        self.state = next_state or self.state
        #print(f'Continue {self.state}')
        return 1


# This is very interesting configuration. But it's good for buys.
# start 3 Levels32(Levels21(StopLevel())) !!!
# start 4, Levels43(Levels32(StopLevel()))
# start 3, Levels32(Levels21(StopLevel()))
# start 2, Levels21(Levels10(StopLevel()))
# start 3, typical scheme small Levels34(Levels45(Levels54(Levels43(Levels32(StopLevel())))))
#                               Levels34(Levels45(Levels43(Levels32(StopLevel()))))
#                               Levels34(Levels43(Levels32(StopLevel())))

# This is very interesting configuration. But it's good for sells.
# start 10 test 11, Levels1011(Levels1112(StopLevel()))
# start 9 or 10, Levels910(Levels1011(StopLevel()))
# start 3 Levels34(Levels45(StopLevel()))


class MurrayLevelBuyFlowSmaller(MurrayLevelsBaseFlow):
    initial = Down(3, 2) | Down(2, 1) | Stop()


class MurrayLevelSellFlowSmaller(MurrayLevelsBaseFlow):
    initial = Up(9, 10) | Up(10, 11) | Stop()


class MurrayLevelsSignal:
    def __init__(self, total_samples, signal_class, trigger_level):
        self.signal = signal_class
        self.trigger_level = trigger_level
        self.total_samples = total_samples
        self.streams = [
            iter(EnumeratedMurrayLevelsStream(total_samples)),
            iter(EnumeratedCandlesStream(total_samples))
        ]

    def move(self):
        (_, murray_levels), (pos, p) = [next(stream) for stream in self.streams]
        if get_murray_level(murray_levels, p.close) == self.trigger_level:
            #print(f'Started verification at position {pos} -----------------------------------------------')
            signal_flow = self.signal(self.total_samples, pos, murray_levels)
            while signal := signal_flow.move():
                if signal == 1:
                    continue
                elif signal == 2:
                    print(f'YAY {pos}')
                    return pos
                else:
                    return -1
        return -1
