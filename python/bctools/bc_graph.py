#!/usr/bin/python
# coding=UTF-8
#
# BitCurator
# 
# This code is distributed under the terms of the GNU General Public 
# License, Version 3. See the text file "COPYING" for further details 
# about the terms of this license.
# 
# This is a python file containing some utility functions for
# generate_reports script

import matplotlib
#import pylab as p

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from bc_utils import filename_from_path, bc_addToReportFileList 
#import bc_utils
from matplotlib.backends.backend_pdf import PdfPages

def bc_generate_bar_graph(PdfReport, image_info, outfile, item_dict):
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1,1,1)

    y = []
    group_labels = []

    ## print("D: Generate_bar_graph: Dict:Length: %d, %s"
                       ## % (len(item_dict), item_dict.items())) 

    # Simple lambda expression to sort the items in ascending order (then reverse it)
    sorted_items = sorted(item_dict.items(), key=lambda x: x[1])
    sorted_items.reverse()
    num_items = 0
    for i in sorted_items:
       y.append(i[1])
       group_labels.append(i[0])
       num_items += 1
       if num_items >= PdfReport.bc_max_formats_in_bar_graph:
           ## print("D: Reporting only %d formats in the bargraph" %num_items)
           break
 
    # calculate the number of bars required
    N = len(y)
    # generate a range of numbers (just a placeholder before we relabel)
    ind = range(N)

    # Make the font small and the xticks vertical
    for label in ax.yaxis.get_ticklabels():
        # label is a Text instance
        label.set_fontsize(6)

    for label in ax.xaxis.get_ticklabels():
        label.set_fontsize(7)
    # set up the actual graphing
    ax.bar(ind,y,width=0.1,facecolor = '#888888',ecolor = 'black')
    ax.set_ylabel('Counts')
    imgname = 'image_filename: ' + str(image_info['image_filename'])
    imgname='Disk Image: '+filename_from_path(imgname)
    ax.set_title(imgname + ' File counts (by format)')
    rects = ax.bar(ind,y,width=0.3,facecolor = '#888888',ecolor = 'black')

    # Write the frequency on top of each bar
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height+1.0, '%d'%int(height), ha='center', va='bottom')

    ax.set_xticks(ind)
    ax.set_xticklabels(group_labels)
    fig.autofmt_xdate()
 
    #pp = PdfPages(outfile)
    canvas.print_figure(outfile)
    bc_addToReportFileList(outfile, PdfReport)

    #pp.savefig(fig)
    #pp.close()
    #os.system("evince ./bc_format_bargraph.pdf")

def bc_draw_histogram_fileformat(PdfReport, image_info, outfile, item_dict):
    bc_generate_bar_graph(PdfReport, image_info, outfile, item_dict)

