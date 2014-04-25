#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# timeslack.py
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

import matplotlib.pyplot as plt
from numpy import exp, pi, sqrt
import random
import sys

sys.path.append('..')
from scheduling import Settings
import scheduling


class Scheduler(scheduling.Scheduler):

    """Scheduler using the Time/Slackness policy."""

    def __init__(self, alpha):
        """Initiate a new scheduler.

            alpha: factor for the slackness part of the density.

        """
        scheduling.Scheduler.__init__(self)
        self.alpha = alpha

    def decision_density(self, red_time, slackness):
        """The Time/Slackness decision density.

        Arguments:
        red_time -- basically (current time / maximum admissible time)
        slackness -- the so called slackness

        """
        p1 = red_time**42
        p2 = self.alpha * (.1 + 2 * (0 < slackness < 1))
        #p2 = slackness if slackness < 1 else max(2 - slackness, 0)
        #p2 = max(0, slackness * (2 - slackness))
        return p1 + (1 - p1) * p2

    def schedule_tasks(self):
        """Schedule all tasks using the Time/Slackness heuristic."""
        next_tasks = list(Settings.tasks)
        for t in range(Settings.nb_slots):
            prev_cost = self.load_profile.get_load(t-1)
            cur_tasks = next_tasks
            next_tasks = []
            for task in cur_tasks:
                red_time = t / float(Settings.nb_slots - task.nb_slots)
                task_area = float(task.inst_cost * task.nb_slots)
                rev_cost = float(Settings.L - prev_cost)
                rev_time = float(Settings.nb_slots - task.nb_slots - t)
                rev_area = rev_cost * rev_time
                slackness = 0
                if rev_area > 0:
                    slackness = task_area / rev_area
                g = self.decision_density
                if random.uniform(0, 1) < g(red_time, slackness):
                    self.schedule_task(task, t)
                else:
                    next_tasks.append(task)


def sample_gc(alpha):
    """Compute GC for a sample run."""
    sched = Scheduler(alpha)
    sched.schedule_tasks()
    return sched.get_global_cost()
