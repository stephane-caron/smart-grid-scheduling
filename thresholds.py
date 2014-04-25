#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# thresholds.py
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
import time

from scheduling import Settings
from strats import aloha, game, timeslack, uniform
import trials

"""Sample test script to find good values of the heuristics' parameters."""

def generic_errorbar(xvals, niter, format, samplefun):
    """Plot errorbars for several runs of an argumentless numerical function.

    Arguments:
    xvals -- domain for the x-axis of the plot
    niter -- number of runs per argument in xvals
    format -- pyplot format for the errorbars
    samplefun -- numerical function with no argument

    """
    mean, dev = trials.get_first_moments(niter, samplefun)
    means, devs = [mean for x in xvals], [dev for x in xvals]
    eb, _, _ = pyplot.errorbar(xvals, means, yerr=devs, lw=2)
    return eb

def uniform_errorbar(xvals, niter):
    """Plot errorbars for the Uniform strategy."""
    return generic_errorbar(xvals, niter, 'm-', uniform.sample_gc)

def game_errorbar(xvals, niter):
    """Plot errorbars for the Game strategy."""
    return generic_errorbar(xvals, niter, 'r-', game.sample_gc)

################################################################################

def param_errorbar(xvals, niter, samplefun, color):
    """Plot errorbars for several runs of samplefun.

    Arguments:
    xvals -- domain for the arguments of samplefun
    niter -- number of runs per argument in xvals
    format -- pyplot format for the errorbars
    samplefun -- numerical one-argument function

    """
    moments = [trials.get_first_moments(niter, samplefun(x)) for x in xvals]
    yvals = [mmt[0] for mmt in moments]
    devs = [mmt[1] for mmt in moments]
    eb, w1, w2 = pyplot.errorbar(xvals, yvals, yerr=devs, marker='o')
    return eb

def aloha_errorbar(xvals, niter):
    """Plot errorbars for the ALOHA-like I policy."""
    samplefun = lambda thr: (lambda: aloha.sample_gc(thr, 0))
    return param_errorbar(xvals, niter, samplefun, 'g')

def aloha2_errorbar(xvals, niter):
    """Plot errorbars for the ALOHA-like II policy."""
    samplefun = lambda thr: (lambda: aloha.sample_gc(thr, .1 * thr))
    return param_errorbar(xvals, niter, samplefun, 'orange')

def timeslack_errorbar(xvals, niter):
    """Plot errorbars for the Time/Slackness policy."""
    samplefun = lambda alpha: (lambda: timeslack.sample_gc(alpha))
    return param_errorbar(xvals, niter, samplefun, 'b')

################################################################################

if __name__ == "__main__":
    Settings.from_file('twoplayers.in')
    xvals = numpy.arange(0, 1.025, 0.025)

    uni_mrk = uniform_errorbar(xvals, niter=42)
    game_mrk = game_errorbar(xvals, niter=20)
    aloha_mrk = aloha_errorbar(xvals, niter=100)
    aloha2_mrk = aloha2_errorbar(xvals, niter=100)
    timeslack_mrk = timeslack_errorbar(xvals, niter=100)

    pyplot.legend([aloha_mrk, aloha2_mrk, uni_mrk, game_mrk, timeslack_mrk],
        ['ALOHA-like I', 'ALOHA-like II', 'Uniform', 'Game', 'TSD Density'],
        loc='lower left', shadow=True, fancybox=True)

    pyplot.ylabel('GC ($)')
    pyplot.xlabel('Param.')
    pyplot.title(Settings.file)
    pyplot.grid(True)
    pyplot.show()
