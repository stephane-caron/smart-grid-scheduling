#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# scheduling.py
# This file is part of DR StratComp.
#
# Copyright (C) 2010 - Stéphane Caron
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#

import matplotlib.pyplot as pyplot
import numpy


class Task:

    """Straightforward jobs representation."""

    def __init__(self, id, d, tau):
        """Constructor for a task.

        Arguments:
        id -- unique identifier
        d -- instant cost
        tau -- duration (number of slotes)

        """

        self.id = id
        self.nb_slots = tau
        self.inst_cost = d

    def duration(self):
        """Compute task's duration in seconds."""
        return (float(self.nb_slots) / Settings.nb_slots) * Settings.T


class Settings:

    """Global settings for the current run.

    All the settings (number of slots, tasks, etc.) are stored in static members
    of this class. Data can be read from input files using the from_file method.

    """

    T = 6. * 3600. # 6 hours, in seconds
    L, nb_slots, C0, C1 = 0, 0, 0, 0
    file = 'default.in'
    tasks = []

    @classmethod
    def from_file(cls, file):
        """Read settings for the current run from a configuration file."""
        Settings.tasks = []
        Settings.file = file
        f = open('settings/' + file, 'r')
        Settings.L = float(f.readline().split()[2])
        Settings.nb_slots = int(f.readline().split()[2])
        Settings.C0 = float(f.readline().split()[2])
        Settings.C1 = float(f.readline().split()[2])
        f.readline() # skip blank line
        nb_lines = int(f.readline().split()[0])
        next_id, jobs_area = 0, 0
        for lid in range(nb_lines):
            line = f.readline()
            num = int(line.split()[0])
            tau = int(line.split()[1])
            d = float(line.split()[2])
            for k in range(num):
                Settings.tasks.append(Task(next_id, d, tau))
                next_id += 1
            jobs_area += num * d * tau
        if jobs_area < Settings.L * Settings.nb_slots:
            print "Warning: non-triviality criterion not met!"
        f.close()

    @classmethod
    def min_cost(cls):
        """Compute the constant part of GC."""
        return Settings.C0 * sum(t.duration() * t.inst_cost
                                 for t in Settings.tasks)


class LoadProfile:

    """Manages insertion/deletion of load on time slots intervals."""

    def __init__(self):
        self.inst_load = dict((t, 0) for t in range(Settings.nb_slots))

    def add_load(self, slot_len, inst_cost, time_slot):
        """Add load on a given time slots interval.

        Arguments:
        slot_len -- lenght of the interval (number of slots)
        inst_cost -- algebraic load to add (can be negative)
        time_slot -- start time slot

        """
        if time_slot < 0 or time_slot + slot_len > Settings.nb_slots:
            raise Exception("Invalid scheduling.")
        for u in range(time_slot, time_slot + slot_len):
            self.inst_load[u] += inst_cost

    def get_load(self, time_slot):
        """Get load at a given time slot."""
        if 0 <= time_slot < Settings.nb_slots:
            return self.inst_load[time_slot]
        else:
            return 0

    def get_par(self):
        """Compute the peak-to-average ratio (PAR) of the load profile."""
        average = sum(self.inst_load.values()) / Settings.nb_slots
        peak = max(self.inst_load.values())
        return peak / average

    def plot(self):
        """Plot the current load profile."""
        xvals = range(Settings.nb_slots)
        yvals = self.inst_load.values()
        pyplot.bar(xvals, yvals, width=1, color='y')
        pyplot.xlabel('Time slot')
        pyplot.ylabel('Load (kW)')
        pyplot.xlim(xmin=0, xmax=Settings.nb_slots)
        pyplot.grid(True)


class Scheduler:

    """Abstract class for a scheduling policy."""

    def __init__(self):
        self._sched_slots = {}
        self.load_profile = LoadProfile()

    def is_scheduled(self, task):
        """Find if a given Task instance has been scheduled yet."""
        return self._sched_slots.has_key(task.id)

    def schedule_task(self, task, time_slot):
        """Schedule a Task instant at given time slot."""
        if not self.is_scheduled(task):
            self.load_profile.add_load(task.nb_slots, task.inst_cost,
                                       time_slot)
            self._sched_slots[task.id] = time_slot
        else:
            raise Exception("Task already scheduled.")

    def reschedule_task(self, task, time):
        """Removes previous scheduling of task if any and schedule it again."""
        if self.is_scheduled(task):
            self.load_profile.add_load(task.nb_slots, -task.inst_cost,
                self.get_task_slot(task))
            del self._sched_slots[task.id]
        self.schedule_task(task, time)

    def utility_cost(self, load):
        """Compute the ramp cost for a given instant load."""
        if load <= Settings.L:
            return Settings.C0
        return Settings.C0 + Settings.C1 * (load - Settings.L)

    def integrate_cost(self, start, stop):
        """Compute the total cost on a given time interval (bounds included)."""
        if 0 <= start <= stop < Settings.nb_slots:
            dt = Settings.T / Settings.nb_slots
            load = lambda t: self.load_profile.get_load(t)
            cost = lambda l: self.utility_cost(l)
            return sum(cost(load(t)) * dt for t in range(start, stop + 1))
        else:
            raise Exception("Invalid integration bounds.")

    def get_task_slot(self, task):
        """Find the time slot when a Task instance is scheduled."""
        try:
            return self._sched_slots[task.id]
        except KeyError:
            raise Exception("Task " + repr(task.id) + " not scheduled.")

    def get_task_cost(self, task):
        """Compute the cost experience by the customer of a given job."""
        time_slot = self.get_task_slot(task)
        return task.inst_cost * \
            self.integrate_cost(time_slot, time_slot + task.nb_slots - 1)

    def get_global_cost(self):
        """Compute the Global Cost experienced by the system."""
        return sum([self.get_task_cost(task) for task in Settings.tasks])
