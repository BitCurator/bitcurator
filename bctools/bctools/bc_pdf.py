#!/usr/bin/python
# coding=UTF-8
#
# BitCurator
# 
# This code is distributed under the terms of the GNU General Public 
# License, Version 3. See the text file "COPYING" for further details 
# about the terms of this license.
# 
# This is a python file containing some utility functions related to fpdf for
# generate_reports script

# Checks if the report has reached the end of page and if so, starts
# a new page. 
def bc_table_end_page(pdf, FiwalkReport, linenum, header, w):
    if ((linenum>=FiwalkReport.max_entries_per_page) & 
        (linenum%FiwalkReport.max_entries_per_page == 0)):
        # Close the page
        pdf.cell(sum(w),0,'','T')
        pdf.add_page()
        for i in range(0,len(header)):
            pdf.cell(w[i],7,header[i],1,0,'C',1)
        pdf.ln()
    FiwalkReport.page = pdf.page

#def make_header(this, logo, header_text):
def make_header(this, header_text):
    this.set_font('Arial','B',14)
    this.underline = 1
    header_text = 'Report: ' + header_text
    this.cell(0,0,header_text,0,0,'L')

    # Logo - disabled right now
    #this.image(logo,150,5,33)

    # Line break
    this.ln(10)

 #
 # Utility Function to Shorten the text length to fit in the cell.
 #

def bc_adjust_text(cell_text, cell_width):
    #
    # Due to the small font used, the len() and the cell width
    # are not using the same unit. Hence making the available
    # space much shorter. The multiplier .3 is chosen from trial-and-error
    # method to use the full width of the column.
    #
    if len(cell_text) > 0.5 * cell_width:
        short_len = 0.3 * cell_width
        
        text = cell_text[0:int(short_len)] + '...' + \
           cell_text[-int(short_len):]
        return text
    return cell_text


