#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# game.py
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

import random
import sys

sys.path.append('..')
from scheduling import Settings
import scheduling


class Scheduler(scheduling.Scheduler):

    """Scheduler implementing the cooperative game between players."""

    def __init__(self, rounds_ratio):
        """Initiate a new scheduler.

        Arguments:
        rounds_ratio -- number of rounds will be len(tasks) * (1 + nb_rounds)
        
        """
        scheduling.Scheduler.__init__(self)
        self.rounds_ratio = rounds_ratio

    def schedule_tasks(self):
        """Make all consumers play reschedule their job once, then play
        additional nb_rounds * len(tasks) rounds where players are selected
        uniformly at random.

        """
        def randslot(task):
            return random.randint(0, Settings.nb_slots - task.nb_slots)
        tasks = list(Settings.tasks)
        slots = dict((t.id, randslot(t)) for t in tasks)
        def play(cur_task):
            #print "play", cur_task.id, "scheduled at time", slots[cur_task.id]
            tau_i = cur_task.nb_slots
            def H_j(other_task, t):
                d_j = other_task.inst_cost
                t_j = slots[other_task.id]
                tau_j = other_task.nb_slots
                DF_j = lambda t: (t_j - tau_i <= t < t_j)
                return (-d_j) * (DF_j(t) - DF_j(t - tau_j))
            H = lambda t: sum(H_j(other_task, t)
                for other_task in tasks if other_task.id != cur_task.id)
            H_dict = dict((t, H(t)) for t in range(Settings.nb_slots))
            #print " ", H_dict
            H_sum = lambda t: sum(H_dict[u]
                                  for u in range(t, Settings.nb_slots))
            H_sums = [H_sum(t) for t in range(Settings.nb_slots - tau_i + 1)]
            #print " ", H_sums
            min_sum = min(H_sums)
            min_pos = [t for t,v in enumerate(H_sums) if v == min_sum]
            new_time = random.choice(min_pos)
            slots[cur_task.id] = new_time
            self.reschedule_task(cur_task, new_time)
        map(play, tasks)
        nb_rounds = len(tasks) * self.rounds_ratio
        for i in range(nb_rounds):
            play(random.choice(tasks))
        #print slots


def sample_gc(ratio=2):
    """Compute GC for a sample run of the game.

    Arguments:
    ratio -- number of additional rounds / number of tasks

    """
    sched = Scheduler(ratio)
    sched.schedule_tasks()
    return sched.get_global_cost()

def sample_par(ratio=2):
    """Compute the PAR for a sample run of the game.

    Arguments:
    ratio -- number of additional rounds / number of tasks

    """
    sched = Scheduler(ratio)
    sched.schedule_tasks()
    return sched.load_profile.get_par()
