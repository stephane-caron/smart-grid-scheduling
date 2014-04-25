DR StartComp
============

DR StratComp stands for Demand-Response Strategies Comparator. Its purpose is
to assess the efficiency of different energy-consumption scheduling algorithms
in a smart power grid.

This is the code associated with the paper *Incentive-based Energy Consumption
Scheduling Algorithms for the Smart Grid*. I wrote it in 2010 during my
internship with Pr George Kesidis at Penn State University. For more
information about this work, see

    https://scaron.info/research/conf/smartgridcomm-2010.html

Installation
============

DR StratComp requires Python 2.4+ with the matplotlib library.

Execution goes through the main.py file:

	% python main.py

Look at the source code to find the different default scenarii available.

Writing your own test case
==========================

Format of the input files is rather loose. First four lines describe (in that
order) the values of L, the number of slots, C0 (constant cost) and C1 (overage
part of the cost function). Lines should look like this:

    L = 3000
    nb_slots = 36
    C0 = 2.8e-6
    C1 = 2.8e-8

Anyway you can add anything you want after you specified the values of the
parameters. Hence, the following syntax is allowed (and recommanded):

    L = 3000 kW
    nb_slots = 36 slots (10 min/slot)
    C0 = 2.8e-6 $/kW/s (slope 1 in the BC Hydro model)
    C1 = 2.8e-8 $/kW^2/s

Total duration is 6 hours (you can change it in scheduling.Settings.T). Energy
units are up to the test file, yet kW should be preferred. Please note that C0
and C1 must use second as "time component" of their units (this has an
incidence on the way costs are computed in scheduling.py).

Rest of the file describes the jobs. Next line indicates the number P of task
"packs". Each of the P following lines describe a pack, and consist in two
integers and a floating point number, respectively the number of jobs, their
duration (in time slots) and their instant cost (in whatever unit you chose for
L), e.g.

    5
    1 15 462.24
    2 30 132.12
    10 10 56.42
    10 20 17.51
    20 10 19.18
