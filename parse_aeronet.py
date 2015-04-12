#!/usr/bin/python

import pkg_resources
pkg_resources.require("matplotlib")

import matplotlib.pyplot as plt
import matplotlib

datafile = "150101_151231_Billerica.lev15"
sitename = "Billerica"

def image_from_data(date_str, data):
    (day, month, year) = date_str.split(":")
    filename = "output/" + sitename + "-" + year + "-" + month + "-" + day + ".png"

    (times, measurements) = zip(*data)

    # theming from https://ryanmlayer.wordpress.com/2014/02/18/matplotlib-black-background/
#    matplotlib.rcParams.update({'font.size': 12})
    fig = matplotlib.pyplot.figure(figsize=(6,4),dpi=100,facecolor='black')
#    fig.subplots_adjust(wspace=.05,left=.01,bottom=.01)
    ax = fig.add_subplot(1,1,1,axisbg='k')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    ax.title.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.tick_params(axis='both', direction='in')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    ax.set_xlabel("Time of Day")
    ax.set_ylabel("AOD 500 Level")
    ax.set_title("Aerosol levels on " + year + "-" + month + "-" + day)

    plt.plot(times, measurements, color='white')
#    plt.savefig(filename, figsize=(6, 4), dpi=100, facecolor="black")
    plt.savefig(filename, bbox_inches='tight', facecolor=fig.get_facecolor(), transparent=True)

    plt.clf()

    print date_str, times, measurements



def parse_time(time_str):
    (hours, minutes, seconds) = time_str.split(":")
    return int(hours) + float(minutes) / 60

with open(datafile, "r") as fh:
    i = 0
    inside_data = False
    current_date = None
    current_data = []

    for line in fh:
        parts = line.split(",")
        if len(parts) <= 0:
            pass

        #print parts
        if parts[0] == "Date(dd-mm-yy)":
            date_index = 0
            time_index = parts.index("Time(hh:mm:ss)")
            aot_500_index = parts.index("AOT_500")
            inside_data = True
            continue

        if inside_data:
            date_str = parts[date_index]
            current_time = parse_time(parts[time_index])
            aot_500 = float(parts[aot_500_index])

            if date_str != current_date:
                if (current_date is not None):
                    image_from_data(current_date, current_data)
                current_data = []
                current_date = date_str

            current_data.append((current_time, aot_500))

#            print date_str, current_time, aot_500

