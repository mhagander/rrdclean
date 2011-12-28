rrdclean
========

Yet another trivial tool to remove spikes from RRD graphs,
showing up in e.g. http://www.munin-monitoring.org/.

What differs it from the others? The main thing is that it's
interactive, prompting you for each individual datapoint before
it's removed. It will also show you the <n> top items to let
you decide on a trigger level for where to ask interactively.

Example session::

 rrdclean.py myfile.rrd
 Read 488 values (rest is NaN)
 154947.60044
 154947.60044
 154947.60044
 10061.387875
 10061.387875
 10061.387875
 10061.387875
 10061.387875
 5734.7344187
 5734.7344187
 5734.7344187
 5734.7344187
 5531.2928506
 5531.2928506
 5531.2928506
 5531.2928506
 5531.2928506
 5484.1866208
 5484.1866208
 5484.1866208
 Enter cutoff value, or blank to see more values: 150000
 Replace value 154947.60044 at  2011-12-27 20:45:00 CET / 1325015100  [y/n]? y
 Ok, replacing
 Replace value 154947.60044 at  2011-12-27 20:45:00 CET / 1325015100  [y/n]? y
 Ok, replacing
 Replace value 154947.60044 at  2011-12-27 20:45:00 CET / 1325015100  [y/n]? y
 Ok, replacing
