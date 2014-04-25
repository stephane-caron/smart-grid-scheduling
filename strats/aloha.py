#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# aloha.py
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
import numpy
import random
import sys

sys.path.append('..')
from scheduling import Settings
import scheduling


class Scheduler(scheduling.Scheduler):

    """Scheduler for the ALOHA-like policy."""

    def __init__(self, prob_safe, prob_overage):
        """Initiate a new scheduler.
        
        Arguments:
        prob_safe -- scheduling probability when there is no overage
        prob_overage -- scheduling probability otherwise

        """
        scheduling.Scheduler.__init__(self)
        self.prob_safe = prob_safe
        self.prob_overage = prob_overage

    def schedule_tasks(self):
        """Schedule all tasks according to the ALOHA-like strategy."""
        def schedule_with_prob(task, slot, p):
            if numpy.random.uniform() < p:
                self.schedule_task(task, slot)
        next_tasks = list(Settings.tasks)
        for time_slot in range(Settings.nb_slots):
            prev_cost = self.load_profile.get_load(time_slot - 1)
            cur_tasks = next_tasks
            next_tasks = []
            for task in cur_tasks:
                if time_slot == Settings.nb_slots - task.nb_slots:
                    self.schedule_task(task, time_slot)
                elif prev_cost + task.inst_cost < Settings.L:
                    schedule_with_prob(task, time_slot, self.prob_safe)
                else:
                    schedule_with_prob(task, time_slot, self.prob_overage)
                if not self.is_scheduled(task):
                    next_tasks.append(task)


def sample_gc(prob_safe, prob_overage):
    """Compute GC for a sample run of an ALOHA-like scheduler."""
    sched = Scheduler(prob_safe, prob_overage)
    sched.schedule_tasks()
    return sched.get_global_cost()
