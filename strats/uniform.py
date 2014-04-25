#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# uniform.py
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

import numpy
import random
import sys

sys.path.append('..')
from scheduling import Settings
import scheduling


class Scheduler(scheduling.Scheduler):

    """Scheduler for the Uniform policy."""

    def __init__(self):
        scheduling.Scheduler.__init__(self)

    def schedule_tasks(self):
        """Schedule all tasks uniformly at random."""
        for task in Settings.tasks:
            time_slot = random.randint(0, Settings.nb_slots - task.nb_slots)
            self.schedule_task(task, time_slot)


def sample_gc():
    """Compute GC for a sample run."""
    sched = Scheduler()
    sched.schedule_tasks()
    return sched.get_global_cost()

def sample_par():
    """Compute the PAR for a sample run."""
    sched = Scheduler()
    sched.schedule_tasks()
    return sched.load_profile.get_par()
