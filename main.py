#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
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
import time

from scheduling import Settings
from strats import aloha, game, timeslack, uniform
import scheduling
import trials


# We found the following parameters to be the best for the number of time slots
# (36) we used in our simulations -- they are actually the same in both the
# domestic and heterogeneous setting. Anyway, they do depend on the time granu-
# larity (number of time slots) since they scale step-to-step probabilities and
# not frequencies.

_ALOHA_1 = .2
_ALOHA_2_SAFE = .145
_ALOHA_2_OVER = .0175
_TIME_SLACKNESS = .06


def compute_moments():
    """Compute first moments (mean and standard deviation) for several runs of
    all the policies available in the strats module.

    """
    game_mmts = trials.get_first_moments(5, game.sample_gc)
    aloha1_mmts = trials.get_first_moments(200, lambda:
        aloha.sample_gc(_ALOHA_1, 0))
    aloha2_mmts = trials.get_first_moments(200, lambda:
        aloha.sample_gc(_ALOHA_2_SAFE, _ALOHA_2_OVER))
    alpha = _TIME_SLACKNESS
    timeslack_mmts = trials.get_first_moments(200, lambda:
        timeslack.sample_gc(alpha))
    uni_mmts = trials.get_first_moments(200, uniform.sample_gc)
    moments = [game_mmts, timeslack_mmts, aloha2_mmts, aloha1_mmts, uni_mmts]
    labels = ['Game', 'Time/Slackness', 'ALOHA-like II', 'ALOHA-like I',
              'Uniform']
    means = map(lambda m: m[0], moments)
    devs = map(lambda m: m[1], moments)
    return means, devs, labels

################################################################################

def plot_gc(means, devs, labels):
    """Plot the GCs (with error bars) for the different policies."""
    yalign = numpy.arange(len(labels))+.5
    plt.barh(yalign, means, xerr=devs, ecolor='r', align='center',
             color=(0, .6, .9), capsize=15)
    plt.yticks(yalign, ('', '', '', ''))
    for i, ylabel in enumerate(labels):
        plt.text(0, .5 + i, '  ' + ylabel, ha='left', va='center',
                 color='white', weight='bold', size='large')
    plt.title(Settings.file + ' (' + repr(len(Settings.tasks)) + ' users)')
    plt.ylabel('Strategy')
    plt.xlabel('GC ($)')
    plt.grid(True)

def plot_load_profile(sched, title):
    """Plot the load profile of a run of a given Scheduler instance."""
    sched.schedule_tasks()
    sched.load_profile.plot()
    plt.axhline(y=Settings.L, xmin=0, xmax=1, color='r')
    plt.ylim(ymin=0, ymax=2*Settings.L)
    plt.title(title)

################################################################################

def example_plot_gc_only():
    """Plot GC for the different policies."""
    means, devs, labels = compute_moments()
    plt.subplot(111)
    plot_gc(means, devs, labels)
    plt.show()

def example_plot_load_profiles():
    """Plot GC and a sample load profile for each policy."""
    means, devs, labels = compute_moments()
    plt.subplot(321)
    plot_gc(means, devs, labels)
    plt.subplot(322)
    plot_load_profile(uniform.Scheduler(),
                      'Uniform Sample')
    plt.subplot(323)
    plot_load_profile(aloha.Scheduler(_ALOHA_1, 0),
                      'ALOHA-like Sample')
    plt.subplot(324)
    plot_load_profile(aloha.Scheduler(_ALOHA_2_SAFE, _ALOHA_2_OVER),
                      'ALOHA-like II Sample')
    plt.subplot(325)
    plot_load_profile(timeslack.Scheduler(_TIME_SLACKNESS),
                      'Time/Slackness Sample')
    plt.subplot(326)
    plot_load_profile(game.Scheduler(2),
                      'Game Sample')
    plt.show()

def example_average_par():
    """Compare the average PAR of each policy."""
    uniform_par_mmts = trials.get_first_moments(100,
        uniform.sample_par)
    aloha1_par_mmts = trials.get_first_moments(100, lambda:
        aloha.sample_gc(_ALOHA_1, 0))
    aloha2_par_mmts = trials.get_first_moments(100, lambda:
        aloha.sample_gc(_ALOHA_2_SAFE, _ALOHA_2_OVER))
    timeslack_par_mmts = trials.get_first_moments(100, lambda:
        timeslack.sample_gc(_TIME_SLACKNESS))
    game_par_mmts = trials.get_first_moments(5,
        game.sample_par)
    print 'Average PAR (mean, std. dev.)'
    print ' - Uniform:', uniform_par_mmts
    print ' - ALOHA-like I:', aloha1_par_mmts
    print ' - ALOHA-like II:', aloha1_par_mmts
    print ' - Time/Slackness:', aloha1_par_mmts
    print ' - Game:', game_par_mmts

def example_uniform_vs_game():
    """Plot a Uniform and a Game load profile."""
    plt.subplot(211)
    plot_load_profile(uniform.Scheduler(),
                      'Uniform Load Profile')
    plt.subplot(212)
    plot_load_profile(game.Scheduler(2),
                      'Game Load Profile')
    plt.show()

################################################################################

if __name__ == "__main__":
    Settings.from_file('heterogeneous.in')
    #example_plot_load_profiles()
    example_plot_gc_only()
    #example_average_par()
    #example_uniform_vs_game()
