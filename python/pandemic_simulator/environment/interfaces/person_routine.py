# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.
import enum
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional, Sequence, Union, Type

from .ids import LocationID
from .location import Location
from .person import Person
from .sim_time import SimTimeInterval, SimTimeTuple, SimTime

__all__ = ['PersonRoutine', 'SpecialEndLoc', 'PersonRoutineWithStatus', 'PersonRoutineAssignment']


class SpecialEndLoc(enum.Enum):
    social = 0


@dataclass(frozen=True)
class PersonRoutine:
    """A dataclass that defines a person's routine every step (hour). """

    start_loc: Optional[LocationID]
    """Start location of the routine. If None, the routine can be started at any location."""

    end_loc: Union[LocationID, SpecialEndLoc]
    """End location of the routine that is either a specific location id or an instance of SpecialEndLoc."""

    valid_time: SimTimeTuple = SimTimeTuple()
    """Specifies the time during which the routine is available to start."""

    start_trigger_time: SimTimeInterval = SimTimeInterval(hour=1)
    """Start trigger time of the routine specified through SimTimeInterval. The routine will only start during
    valid_time, and once triggered the routine will be queued to be executed at some point while it remains valid.
    Default is set to be triggered to start every hour during valid_time."""

    start_hour_probability: float = 0.9
    """The probability for starting the routine around the trigger interval."""

    explorable_end_locs: Sequence[LocationID] = ()
    """A collection of end locations of the routine to explore with the probability given by
     `explore_probability`."""

    explore_probability: float = 0.05
    """Exploration probability to pick one of the explorable_end_locs instead of end_loc."""

    duration_of_stay_at_end_loc: int = 1
    """Specifies the duration (in hours) to stay at the end location."""

    repeat_interval_when_done: SimTimeInterval = SimTimeInterval(day=1)
    """Specifies the interval to repeat the routine when completed"""


@dataclass
class PersonRoutineWithStatus:
    """A mutable dataclass that maintains status variables of a routine to make it stateful."""

    routine: PersonRoutine
    due: bool = False
    started: bool = False
    duration: int = 0
    done: bool = False
    end_loc_selected: Optional[LocationID] = None
    """The final end_loc selected after sampling from routine.explorable_end_locs"""

    def _is_routine_due(self, sim_time: SimTime) -> bool:
        if self.started or self.done or sim_time not in self.routine.valid_time:
            # not due if the routine has already started or is completed or is not valid
            return False

        return self.due or self.routine.start_trigger_time.trigger_at_interval(sim_time)

    def sync(self, sim_time: SimTime) -> None:
        """Sync the status variables with time."""
        # if completed check if you need to reset the routine for a repetition
        if self.done and self.routine.repeat_interval_when_done.trigger_at_interval(sim_time):
            self.reset()

        self.due = self._is_routine_due(sim_time)

    def reset(self) -> None:
        """Reset status variables"""
        self.due = False
        self.started = False
        self.duration = 0
        self.done = False
        self.end_loc_selected = None


class PersonRoutineAssignment(metaclass=ABCMeta):
    """A callable interface for person routine assignment for the given person"""

    @property
    @abstractmethod
    def required_location_types(self) -> Sequence[Type[Location]]:
        pass

    @abstractmethod
    def __call__(self, persons: Sequence[Person]) -> None:
        pass
