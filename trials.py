#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# trials.py
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

from numpy import sqrt

"""Statistics on multiple runs of given numerical functions."""

def get_first_moments(niter, expfun):
    """Compute mean and standard deviation for multiple runs of expfun.

    Arguments:
    niter -- number of runs
    expfun -- numerical function to test

    """
    costs = [expfun() for i in range(niter)]
    mean = sum(costs) / niter
    var = sum([(c - mean)**2 for c in costs]) / niter
    return mean, sqrt(var)

def get_best_over(xvals, samplefun, niter, print_means=False):
    """Returns the best mean over multiple runs on each point of xvals.

    Arguments:
    xvals -- samplefun's arguments' domain
    samplefun -- numerical one-argument function
    niter -- number of iteration per argument in xvals
    print_means -- print means at each point of xvals

    """
    wrapfun = lambda thr: (lambda: samplefun(thr))
    moments = [get_first_moments(niter, wrapfun(thr)) for thr in xvals]
    if print_means:
        print "get_best_over: means:", map(lambda m: m[0], moments)
    best_mean = min(m[0] for m in moments)
    best_mmts = filter(lambda m: m[0] == best_mean, moments)
    return best_mmts[0]
