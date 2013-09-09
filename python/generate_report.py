#!/usr/bin/python
# coding=UTF-8
#
# BitCurator
# Copyright (C) 2012
# All rights reserved.
#
# This code is distributed under the terms of the GNU General Public
# License, Version 3. See the text file "COPYING" for further details
# about the terms of this license.
#
from __future__ import with_statement

__version__ = "1.3.0"

b'This module needs Python 2.7 or later.'
import zipfile,os,os.path,glob,codecs
from fpdf import *
import re
import os
import fnmatch
from collections import namedtuple
import string
import datetime
import sys
import bc_utils
import bc_config
import bc_pdf
import bc_graph
import bc_regress
from bc_utils import filename_from_path
from bc_genrep_dfxml import bc_process_xmlfile_using_sax
from bc_genrep_dfxml import bc_get_volume_info_from_sax
from bc_genrep_text import bc_process_textfile
from bc_genrep_xls import bc_generate_xlsx
from bc_gen_feature_rep_xls import bc_generate_feature_xlsx
import bc_genrep_gui
from PyQt4 import QtCore, QtGui

try:
    from argparse import ArgumentParser
except ImportError:
    raise ImportError("This script requires ArgumentParser which is in Python 2.7 or Python 3.0")

# A list of the report files is maintained, to keep track of which ones
# are actually reported, based on the configuration.
reportFiles = 0

'''
image_fileinfo = ['image_filename', 'partition', 'sectorsize','pagesize','acquisition_seconds', 'partition_offset','block_size','ftype','ftype_str','block_count','first_block','last_block']

image_info = {'image_filename':0, 'partition':0, 'sectorsize':0,'pagesize':0,'acquisition_seconds':'', 'partition_offset':0,'block_size':0,'ftype':0,'ftype_str':0,'block_count':0,'first_block':0,'last_block':0}
'''
# Info about the complete image
image_fileinfo = ['image_filename', 'partitions'] 
image_info = {'image_filename':0, 'partitions':0} 
prtn_info_items = ['partition_offset','block_count','first_block','last_block', 'block_size','ftype','ftype_str']
prtn_info = {'partition_offset':0,'block_count':0,'first_block':0,'last_block':0, 'block_size':0,'ftype':0,'ftype_str':0}

# A list of individual partition information.
glb_image_info = []

#
# Class PDF_BE to write the report to a PDF file.
# It uses the Bulk-Extractor output information as its input.
# It uses the python-3 port of FPDF software from
# https://bitbucket.org/cyraxjoe/py3fpdf.
#
class PDF_BE(FPDF):
    def header(this):
        bc_pdf.make_header(this,PdfReport.logo, 'Bulk Extractor Features')

    # Page footer
    def footer(this):
        # Position at 1.5 cm from bottom
        this.set_y(-15)
        # Arial italic 8
        this.set_font('Arial','I',8)
        # Page number
        this.cell(0,10,'Page '+str(this.page),0,0,'C')
    
    #
    # This function builds the table for reporting the information
    # gathered from the feature files created by bulk-extractor
    #
    def make_table_be(self, header,filename):
        self.set_text_color(20)
        self.set_font('Times','I',10)

        self.underline = 1
        self.set_x(10)
        self.cell(0, 10, 'Abbreviation Key:', border=0, ln=1)
        self.underline = 0
        self.set_x(10)
        self.cell(0, 5, 'FLTF: Total features located to files', border=0, ln=1)
        self.set_x(10)
        self.cell(0, 5, 'FUTF: Total features unallocated to files', border=0, ln=1)
        self.set_x(10)
        self.cell(0, 5, 'FIER: Total features in encoded regions', border=0, ln=1)
                
        #Colors, line width and bold font
        self.set_fill_color(135,0,0)
        self.set_text_color(255)
        self.set_draw_color(128,0,0)
        self.set_line_width(.3)
        self.set_font('','B')

        #Header (hardcoded columb width)
        w=[50,30,20,20,20]

        for i in range(0,len(header)):
            self.cell(w[i],7,header[i],1,0,'C',1)
        self.ln()

        #Color and font restoration
        self.set_fill_color(224,235,255)
        self.set_text_color(0)

        fill=0
        self.set_font('Times','',12)

        data=[]
        with open(filename) as file_:
            for line in file_:
                data += [line[:-1].split(';')]

        for row in data:
            self.cell(w[0],6,row[0],'LR',0,'L',fill)
            self.cell(w[1],6,row[1],'LR',0,'C',fill)
            self.cell(w[2],6,row[2],'LR',0,'C',fill)
            self.cell(w[3],6,row[3],'LR',0,'C',fill)
            self.cell(w[4],6,row[4],'LR',0,'C',fill)
            self.ln()
            fill=not fill
        #Closure line
        self.cell(sum(w),0,'','T')

    def bc_write_column(self, w,h,cell_text, fill):
        text = bc_pdf.bc_adjust_text(cell_text, w)
        self.cell(w,h,text,'LR',0,'L',fill)

    def bc_get_data_from_feature_file(self, feature_file):
        data=[]
        linenum = 0

        with open(feature_file) as file_:
            for line in file_:
                if bc_utils.is_comment_line(line):
                    continue
                linenum+=1

                if (re.match("Total",line) or \
                    re.match("Unicode Encode Errors",line) or \
                    re.match("Unicode Decode Errors", line)):
                    continue
            
                data += [line[:-1].split('\t')]
                lendir = len(PdfReport.annotated_dir) + 1 + 10 # Adding /annotated
                feat_filename = feature_file[lendir:-4]
           
                # Config file sets the maxlines to 0 to report all the lines
                if (PdfReport.bc_config_feature_lines[feat_filename] != 0):
                    if (linenum >= PdfReport.bc_config_feature_lines[feat_filename]):
                        # Lines reached max: Breaking
                        break
        return data


    #
    # make one table/xlsx-file per feature
    #
    def make_table_feat_xls(self, feature_file):

        # Get the data from the input file
        data = self.bc_get_data_from_feature_file(feature_file)

        # Now generte the xlsx file for feature file
        bc_generate_feature_xlsx(PdfReport, data, feature_file)

    #
    # make one table/pdf-file per feature
    #
    def make_table_feat_pdf(self, feature_file, header):
        # Get the data from the input file
        data = self.bc_get_data_from_feature_file(feature_file)

        # Now generate the pdf file for the feature file
        self.bc_generate_feature_reports_in_pdf(PdfReport, data, feature_file)

    def bc_generate_feature_reports_in_pdf(self, PdfReport, data, feature_file):
 
        header = ['Filename', 'Position','Feature ']

        self.set_text_color(1)
        self.set_font('Times','B',12)
           
        fill=0

        self.cell(40, 7, 'Feature File: ' + \
             filename_from_path(feature_file), border=0, ln=1)
        self.set_font('Times','',8)
        self.underline = 0
        self.set_fill_color(224,235,255)
        self.set_text_color(0)
        self.set_draw_color(128,0,0)
        self.set_line_width(.3)

        # Filename; position; feature
        w=[65,50,75]

        for i in range(0,len(header)):
            self.cell(w[i],7,header[i],1,0,'C',1)
        self.ln()
        linenum = 0
        for row in data:
            # Skip the lines with known text lines to be eliminated
            if (re.match("Total features",str(row))):
                continue

            filename = "Unknown"
            feature = "Unknown"
            position = "Unknown"
           
            # Some lines in the annotated_xxx.txt have less than three
            # columns where filename or feature may be missing.
            if len(row) > 3:
                filename = row[3]
            else:
                filename = "Unkown"

            if len(row) > 1:
                feature = row[1]
            else:
                feature = "Unkown"

            position = row[0]

            # If it is a special file, check if the user wants it to
            # be repoted. If not, exclude this from the table.
            if (PdfReport.bc_config_report_special_files == False) and \
                            (bc_utils.is_special_file(filename)):
                ## print("D: File %s is special. So skipping" %(filename))
                continue
            self.bc_write_column(w[0],6,filename,fill)
            self.bc_write_column(w[1],6,position,fill)
            self.bc_write_column(w[2],6,feature,fill)
            self.ln()
            fill=not fill

            # Start from a new page with header names once
            # reached max_entries allowed per page.
            if ((linenum >= FiwalkReport.max_entries_per_page) &
                    (linenum%FiwalkReport.max_entries_per_page == 0)):
            
                bc_pdf.bc_table_end_page(self, FiwalkReport, linenum, header, w)
            linenum+=1

        #Closure line
        self.cell(sum(w),0,'','T')
        return

#
# Class PDF to write the Fiwalk report to a PDF file.
# It uses the python-3 port of FPDF software from
# https://bitbucket.org/cyraxjoe/py3fpdf.
#
class PDF(FPDF):
    # Page footer
    def header(this):
        bc_pdf.make_header(this,PdfReport.logo, 'File System Statistics and Files')

    # Page footer
    def footer(this):
        # Position at 1.5 cm from bottom
        this.set_y(-15)
        # Arial italic 8
        this.set_font('Arial','I',8)
        # Page number
        this.cell(0,10,'Page '+str(this.page),0,0,'C')

    def set_table_hdr_attributes(self, w, header):
        self.set_font('Times','B',10)
        self.set_fill_color(200,0,0)
        self.set_text_color(255)
        self.set_draw_color(128,0,0)
        self.set_line_width(.3)
        self.set_font('','B')

        for i in range(0,len(header)):
            self.cell(w[i],7,header[i],1,0,'C',1)
        self.ln()
               
    def set_table_body_attributes(self):
        self.set_fill_color(224,235,255)
        self.set_text_color(0)
        self.set_font('Times','',8)

    #
    # Get the "long form" of the "short form" of the format :-)
    # Uses info from the two structures dictFileFmtVal and bcFmtDict.
    # The two structures could be combined into one in the future.
    #
    def bc_get_LongformFmt(self, short_form_fmt):
        for x in FiwalkReport.dictFileFmtVal:
            if x == short_form_fmt:
                for y in FiwalkReport.bcFmtDict:
                    if x == FiwalkReport.bcFmtDict[y]:
                        return (y)

    #
    # This tabe will have the translation of the long and short forms
    # of the format name and the number of files for each format. This
    # has the supplemental information for the bar chart and combines
    # the information fron from dictFileFmtVal and bcFmtDict.
    #
    def bc_make_table_fileformat(self, header, dictFileFmtVal, bcFmtDict):
        # Header
        w=[120,50,20]
    
        self.set_font('Times','B',12)
        self.underline = 1
        self.cell(0, 6, 'File Format Table', ln=1)
    
        self.set_font('Times','',10)
        imgname = 'image_filename: ' + str(image_info['image_filename'])
        
        self.cell(0, 6, 'Disk Image: '+filename_from_path(imgname), ln=1)
        
        #Colors, line width and bold font
        self.set_table_hdr_attributes(w, header)
        
        #Color and font restoration
        self.set_table_body_attributes()
        
        fill=0
        self.set_font('Times','',10)

        # print("D:", dictFileFmtVal)
        # print("D:", bcFmtDict)
        self.bc_get_LongformFmt("PDP-11")

        num_items = 0
        for i in dictFileFmtVal:
            num_items += 1
            trimmed_text = bc_pdf.bc_adjust_text(self.bc_get_LongformFmt(i), w[0])
            self.cell(w[0],6,trimmed_text,'LR',0,'L',fill)
            self.cell(w[1],6,i,'LR',0,'L',fill)
            self.cell(w[2],6,str(dictFileFmtVal[i]),'LR',0,'C',fill)
            self.ln()
            fill=not fill
            bc_pdf.bc_table_end_page(self, FiwalkReport, num_items, header, w)

        # Closure line
        self.cell(sum(w),0,'','T')
        
                
    #
    # This function builds the table for reporting the overall statistics
    # Source : fiwalk
    #
    def make_table_stat(self, header):
        # Header
        w=[70,80]

        self.set_font('Times','B',12)
        self.underline = 1
        self.cell(0, 6, 'Technical Metadata', ln=1)
        self.set_font('Times','I',11)
        self.underline = 0
        if (FiwalkReport.numPartitions == 1):
            prtn = 'Partition'
        else:
            prtn = 'Partitions'
        self.cell(0, 6, 'Found '+ str(FiwalkReport.numPartitions) + ' ' + prtn + ' in this disk', ln=1)
              
        self.set_font('Times','',10)
        imgname = 'image_filename: ' + str(image_info['image_filename'])

        self.cell(0, 6, 'Disk Image: '+filename_from_path(imgname), ln=1)

        # Colors, line width and bold font
        self.set_table_hdr_attributes(w, header)

        # Color and font restoration
        self.set_table_body_attributes()

        # Per partition info now:
        for i in range(0, FiwalkReport.numPartitions):
          fill=0
          self.set_font('Times','',12)
          self.cell(w[0], 6, 'Partition','LR',0,'L',fill) 
          self.cell(w[1], 6, str(i+1), 'LR',0,'L',fill) 
          self.ln()
          fill=not fill

          ## First write all the information from glb_image_info
          self.set_font('Times','',10)
          current_prtn = glb_image_info[i]

          # Display just the file name for the "image_filename" key
          for j in range(0, len(prtn_info_items)):
            key = prtn_info_items[j]
            cell_text = current_prtn[key]
            if (cell_text == 0):
              continue

            self.cell(w[0],6,bc_utils.stringfix(key),'LR',0,'L',fill)
            self.cell(w[1],6,cell_text,'LR',0,'L',fill)
            self.ln()
            fill=not fill

          self.cell(w[0],6,"Number of Files",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.numfiles[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill

          self.cell(w[0],6,"Total Directories",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.dirs[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill
              
          self.cell(w[0],6,"Total Deleted Files",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.deletedFiles[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill
              
          self.cell(w[0],6,"Total Unused Files",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.unusedFiles[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill
              
          self.cell(w[0],6,"Files with Nlinks > 1",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.moreNumlinks[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill
              
          self.cell(w[0],6,"Empty Files ",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.emptyFiles[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill
              
          self.cell(w[0],6,"Big Files(> 1 MB) ",'LR',0,'L',fill)
          self.cell(w[1],6,str(FiwalkReport.bigFiles[i]),'LR',0,'L',fill)
          self.ln()
          fill=not fill
          self.cell(sum(w),0,'','T')

          ## Go to the next page and set up the header if this is not
          ## the last page
          if i < FiwalkReport.numPartitions-1:
            self.add_page()
            for j in range(0,len(header)):
              self.cell(w[j],7,header[j],1,0,'C',1)
            self.ln()
          fill=not fill

        # Closure line
        #self.cell(sum(w),0,'','T')

    #
    # Make a Table of all the Deleted Files
    #
    def make_table_delfiles(self, header):

        self.set_font('Times','B',16)
        self.underline = 1
        self.cell(0, 12, "Deleted Files", border=0, ln=1)
        self.underline = 0
        self.set_font('Times','B',10)
        imgname = 'Disk Image: ' + filename_from_path(image_info['image_filename'])
        self.cell(40, 7, imgname, border=0, ln=1)

        # Set Colimn width
        w = [12,150]

        #Colors, line width and bold font
        self.set_table_hdr_attributes(w, header)

        #Color and font restoration
        self.set_table_body_attributes()

        fill=0
        num_deleted_files = 0
        for i in range(0, len(FiwalkReport.fiDictList)):
            if FiwalkReport.fiDictList[i]['unalloc']:
                num_deleted_files+=1
                ## print("D: Deleted File: ",
                ## num_deleted_files,FiwalkReport.fiDictList[i]['filename'])
                ##self.cell(w[0],6,str(num_deleted_files),'LR',0,'L',fill)
                partition = FiwalkReport.fiDictList[i]['partition']
                self.cell(w[0],6,str(partition),'LR',0,'L',fill)
                mystr = (FiwalkReport.fiDictList[i]['filename'])
                text = bc_pdf.bc_adjust_text(mystr, w[1])
                self.cell(w[1],6,text,'LR',0,'L',fill)
                self.ln()
                fill=not fill
                bc_pdf.bc_table_end_page(self, FiwalkReport, num_deleted_files, header, w)
             
        #Closure line
        self.cell(sum(w),0,'','T')
    
    #
    # Make a Table of all the files with the given format type
    # Full format is what appears in the image file.
    #
    #def make_table_fmtfiles(self, header, file_format):
    def make_table_fmtfiles(self, header, file_format):
        imgname = 'image_filename: ' + str(image_info['image_filename'])
        format_heading = 'Format: '+file_format

        # Write the headlines for the table:
        self.underline = 1
        self.set_font('Times','B',10)
        self.cell(0, 6, 'Disk Image: '+filename_from_path(imgname), ln=1)
        self.cell(0, 12, format_heading, border=0, ln=1)
        self.underline = 0

        # Set Colimn width
        w = [16,150]

        #Colors, line width and bold font
        self.set_table_hdr_attributes(w, header)

        #Color and font restoration
        self.set_table_body_attributes()
            
        fill=0
        num_files = 0

        for i in range(0, len(FiwalkReport.fiDictList)):
            if (FiwalkReport.xmlInput == True):
                mystr = FiwalkReport.fiDictList[i]['libmagic']
            else:
                mystr = bc_utils.normalize(FiwalkReport.fiDictList[i]['libmagic'])

            if mystr == file_format:
                num_files+=1
                ###self.cell(w[0],6,str(num_files),'LR',0,'L',fill)
                self.cell(w[0],6,str(FiwalkReport.fiDictList[i]['partition']),'LR',0,'L',fill)
                mystr = (FiwalkReport.fiDictList[i]['filename'])
                text = bc_pdf.bc_adjust_text(mystr, w[1])
                self.cell(w[1],6,text,'LR',0,'L',fill)
                self.ln()
                fill=not fill
                bc_pdf.bc_table_end_page(self, FiwalkReport, num_files, header, w)
        self.cell(sum(w),0,'','T')
        return

    #
    # Makes a consolidated report of chosen few attributes
    # of all the files listed by fiwalk
    #
    def make_table(self, header):
        self.set_text_color(10)

        self.set_font('Times','I',10)
        self.underline = 0
        self.set_x(-80)
        self.cell(0, 6, "Note: ", border=0, ln=1)
        self.set_x(-80)
           
        self.cell(0, 5, "DIR: Directory:d; Regular file:r", border=0, ln=1)
        self.set_x(-80)
        self.cell(0, 5, "Size: Size of the file in bytes", border=0, ln=1)
        self.set_x(-80)
        self.cell(0, 5, "Deleted: If the file is Deleted ", border=0, ln=1)

        #Header
        w=[60,20,10,15,12,80]

        #Colors, line width and bold font
        self.set_table_hdr_attributes(w, header)

        #Color and font restoration
        self.set_table_body_attributes()
    
        fill=0

        # Warn the user if the length of a feature file is > max lines
        if PdfReport.bc_max_lines_to_report and \
             FiwalkReport.array_ind > PdfReport.bc_config_report_lines['FiwalkReport']:
            print("### WARNING ### Feature Report file has exceeded "\
                    "%d lines limit###" \
                    %(PdfReport.bc_config_report_lines['FiwalkReport']))

        self.set_font('Times','',8)
        linenum = 0
        for i in range(0, FiwalkReport.array_ind-1):
            column = 6
            cell_text = FiwalkReport.fiDictList[i]['filename']

            # Check if config file is set to not report special files
            if (PdfReport.bc_config_report_special_files == False) \
                and (bc_utils.is_special_file(cell_text)):
                ## print("D: File %s is special. Skipping" %(cell_text))
                continue
 
            # Config file sets the maxlines to 0 to report all the lines
            # or a specific number to limit the reporting lines.
            if (PdfReport.bc_config_report_lines['FiwalkReport'] != 0):
                if (linenum >= PdfReport.bc_config_report_lines['FiwalkReport']):
                    # Lines reached max: Breaking
                    print("FiwalkReport: Exceeded Maxlines: ", linenum)
                    break
                    
            linenum += 1
            
            # Just print the filename if the path exceeds cell width
            if (len(cell_text) > w[0]/2):
                cell_text = filename_from_path(cell_text)
            text = bc_pdf.bc_adjust_text(cell_text, w[0])
            self.cell(w[0],6,text,'LR',0,'L',fill)

            self.cell(w[1],column,FiwalkReport.fiDictList[i]['partition'],'LR',0,'L',fill)
            self.cell(w[2],column,FiwalkReport.fiDictList[i]['name_type'],'LR',0,'L',fill)
            self.cell(w[3],column,FiwalkReport.fiDictList[i]['filesize'],'LR',0,'L',fill)
            if FiwalkReport.fiDictList[i]['unalloc']:
                self.cell(w[4],column,'YES','LR',0,'C',fill)
            elif FiwalkReport.fiDictList[i]['alloc']:
                self.cell(w[4],column,'NO','LR',0,'C',fill)

            cell_text = str(FiwalkReport.fiDictList[i]['libmagic'])
            trimmed_text = bc_pdf.bc_adjust_text(cell_text, w[5])
            self.cell(w[5],column,trimmed_text,'LR',0,'L',fill)
            
            self.ln()
            fill=not fill

            # Start from a new page with header names once
            # reached max_entries allowed per page.
            bc_pdf.bc_table_end_page(self, FiwalkReport, i, header, w)

        # Closure line
        self.cell(sum(w),0,'','T')

#
# This function creates a report file for the feature specified
# by the annotated_file.
#
def be_create_pdf_report_file(input_file, annotated_file):
    # Table column headers
    tab_header_feat = ['Filename', 'Position','Feature ']

    pdf = PDF_BE()
    pdf.compress = False
    pdf.add_page()
    pdf.make_table_feat_pdf(input_file,tab_header_feat)

    # Name the pdf file: Remove the first 10 characters: "annotated_"
    # and the last 4 characters: ".txt" and add :.pdf" in the suffix.
    # First create a new directory
    pdf_file = PdfReport.featuredir +'/' + annotated_file[10:-3] + 'pdf'
    pdf.output(pdf_file,'F')
    bc_utils.bc_addToReportFileList(pdf_file, PdfReport)
    return(pdf_file)

def be_create_xlsx_report_file(input_file, annotated_file):

    pdf = PDF_BE()
    pdf.compress = False
    pdf.add_page()
    
    pdf.make_table_feat_xls(input_file)

#
# Class PdfReport:
#
class PdfReport:
    reportFiles = 0
    logo = "/usr/share/pixmaps/bitcurator/FinalBitCuratorLogo-NoText.png" # Default
 
    default_config = False
    bc_config_feature = {}
    bc_config_feature_lines = {}
    bc_config_report_special_files = True
    bc_max_featfiles_to_report = 10
    bc_max_fmtfiles_to_report = 0
    bc_max_lines_to_report = 0
    bc_max_formats_in_bar_graph = 20
    bc_feature_output_in_pdf = 0 # Feature file outputs are in xlsx by default
    
    # Feature file reports: Two separeate sets are maintained - one for
    # feature report files (bc_config_feature) and one for all the
    # rest (bc_config_report_files). The latter is a fixed
    # set, whereas the number of feature report files depends on the bulk-
    # extractor output (and hence the aff image in question).

    # The elements of bc_config_feature specify a flag to indicate
    # if the user wants to report that feature. Another set,
    # bc_config_report_lines, lets the user set how many lines of each
    # feature they want to be idsplayed in the report.

    # The following is a set of all non-feature pdf report files. It is a
    # growing set. Add more as and when new reports are added.
    bc_config_report_files = {'bc_format_bargraph':0,'FiwalkReport':0, \
                              'FiwalkDeletedFiles':0,'BeReport':0}

    # The following is a corresponding set with the number of lines
    # to be reported in each file, being the value of each element.
    bc_config_report_lines = {'bc_format_bargraph':0,'FiwalkReport':0, \
                              'FiwalkDeletedFiles':0,'BeReport':0}

    def __init__(self, in_dir, out_dir, use_config_file, config_file):
 
        import os.path,glob
        self.name = in_dir
        default_config = False

        if os.path.isdir(in_dir):
            self.dname = in_dir
            self.files = set([os.path.basename(x) for x in glob.glob(os.path.join(in_dir,"*.txt"))])

            num_features = len(self.files)
            temp_feature_list = list(self.files)
        else:
            print(">>> File %s does not exist" % in_dir)
            exit(1)

        # outdir should not exist. Flag error if it does
        if os.path.exists(out_dir):
            raise RuntimeError(out_dir+" exists")
            exit(1)
        else:
            os.mkdir(out_dir)

        # Open the Configuration File: If it doesn't exist, default
        ####if use_config_file == 'Y' or use_config_file == 'y':
        #### NOTE: We no longer ask the user to provide or not the config file
        if (os.path.exists(config_file) == False):
            print("Info: Config file %s does not exist. Using Default parameters" %config_file)
            default_config = True
        else:
            default_config = False

        # Initialize the array now that we know the number of elements
        for i in range(0,len(self.files)):
            filename = temp_feature_list[i]

            # ex: annotated_email.txt ==> email
            filename = filename[10:-4]
            self.bc_config_feature[filename] = 0
            self.bc_config_feature_lines[filename] = 0

        if default_config == False:
            #bc_config.bc_parse_config_file(self, config_file)
            bc_config.bc_parse_config_file(PdfReport, FiwalkReport, config_file)
        else:
            # Default config: Report all the feature files and
            # all of the non-feature files
            print("Info: Config file %s does not exist. Using default configuration " %config_file)
            report_features = len(temp_feature_list)

            for i in range(0,report_features-1):
                filename = temp_feature_list[i]

                # ex: annotated_email.txt ==> email
                filename = filename[10:-4]
                self.bc_config_feature[filename] = 1

            self.bc_config_report_files['bc_format_bargraph'] = 1
            self.bc_config_report_files['FiwalkReport'] = 1
            self.bc_config_report_files['FiwalkDeletedFiles'] = 1
            self.bc_config_report_files['BeReport'] = 1
                    

        ## print("D: Reporting the following files: ")
        ## print(self.bc_config_feature)
        ## print(self.bc_config_feature_lines)
        ## print(self.bc_config_report_files)
        ## print(self.bc_config_report_lines)

        # Print out a warning if the number of feature files exceeds limit
        if PdfReport.bc_max_featfiles_to_report and \
              num_features > PdfReport.bc_max_featfiles_to_report:
            print("### WARNING ### The number of features exceeds %d ###"
                              %(PdfReport.bc_max_featfiles_to_report))

    def open(self,fname,mode='r'):
        print("DEBUG: OPEN= %s " % fname, self);
            
    #
    # Generate feature report files using the per-feature text files
    # generated by bulk-extractor
    #
    def be_process_generate_report(self, fn, display_option1):
        PdfReport.annotated_dir = fn.annotated_dir
        PdfReport.outdir = fn.outdir

        # Put the feature files under a separate folder under outdir
        os.mkdir(PdfReport.outdir + '/features')
        PdfReport.featuredir = PdfReport.outdir + '/features'

        # A temporary text file is created to extract some statistics
        # information from the feature files, before moving this information
        # into a table. It is named using the output directory name.

        # The annotated file for each feature has its last 7 lines under
        # comments, four of which have some statistical information
        # used for reporting. So just these lines are extracted, and
        # put in a temporary file fn.outdir.txt. 

        ofn = fn.outdir + ".txt"
        of = open(ofn,"wb")

        # go through every line of each annotated file, look for
        # the pattern and write to the report file.
        for annotated_file in self.files:
            input_file = fn.annotated_dir + '/' + annotated_file

            # Look at the config file to see if the user wants a
            # report file. If not, skip to the next feature.
            feature = annotated_file[10:-4]
            if PdfReport.bc_config_feature[feature] == 0:
                ## NOT Reporting this feature
                continue

            print (">> Generating final report file for feature", feature)

            ifd = open(input_file, "r")
            linenumber = 0
            of.write(bytes(annotated_file, 'UTF-8'))
            of.write(b";")

            # Extract the last 1K characters block which includes the last
            # seven lines.
            with open(input_file, "r") as f:
                f.seek(0,2)          # Seek @ EOF
                fsize = f.tell()     # Get size
                f.seek(max(fsize-1024, 0), 0)   # Set pos at last 1024 chars
                lines = f.readlines()           # Read to end

            lines = lines[-7:]       # Get last 7 lines

            for line in lines:
                linenumber+=1

                # print("D: Line: ", line[2:])
                bc_utils.match_and_write(of, line[2:], "Total features input", 1)
                bc_utils.match_and_write(of, line[2:], "Total features located to files", 1)
                bc_utils.match_and_write(of, line[2:], "Total features in unallocated space" ,1)
                bc_utils.match_and_write(of, line[2:], "Total features in encoded regions", 0)

                if ((fnmatch.fnmatch(line, 'Total*') or
                    (fnmatch.fnmatch(line, 'Unicode*')))):
                    continue

            # Create a report file in xls form (by default) for this feature
            be_create_xlsx_report_file(input_file, annotated_file)
            
            # Create the same report in PDF only if requested by the user.
            if PdfReport.bc_feature_output_in_pdf == True:
                pdf_file = be_create_pdf_report_file(input_file, annotated_file)
                
        of.close()
        return


#
# This class is used to report information from the output file created
# by fiwalk program with -T option.
#
class FiwalkReport:
    numfiles = []
    files = 0
    dirs = []
    deletedFiles = []
    unusedFiles = []
    moreNumlinks = 0
    emptyFiles = []
    bigFiles = []
    numFormats = 0
    dict_array = ["filename", "partition", "id", "name_type", "filesize", \
                  "alloc", "unalloc", "used", "inode", "meta_type", "mode", \
                  "nlink", \
                  "uid", "gid", "mtime", "mtime_txt", "ctime", "ctime_txt",\
                  "atime", "atime_txt", "crtime", "crtime_txt", "libmagic", "seq"]
    dict_val = {}
    fiDictList = []
    bcFmtDict = {}
    dictFileFmtVal = {}
    xmlInput = True
    noLibMagic = False
    regressionTest = False
    regress_annotated_dir = []
    regress_input_xml_file = []
    regress_outdir = []
    regress_beinfo_file = []
    numPartitions = 0
    prevPartition = 1

    # The file format names are very lengthy and hence using these names
    # as they are from the fiwalk output files makes the barchart look ugly.
    # But defining a short form for each format gets tough since the formats
    # are ready dynamically. So a static array like the following is maintained
    # with some known format names mapped to their shorter forms. Those that are
    # not here, will have a short name formed dynamically, with first and last
    # few characters of the lenghty format name. The purpose of the following
    # static table is to have at least some meaningful names in the bar graph.
    dictFileFmtStatic = \
         {'empty':'empty','data':'data','none':'none',\
          'AppleDouble encoded Macintosh file':'AppleDouble',\
          'XML document text':'XML',\
          'SQLite 3.x database':'SQLite3x',\
          'Non-ISO extended-ASCII text, with no line terminators':'nISO-EA-NLT',\
          'Non-ISO extended-ASCII text':'nISO-EA',\
          'Hitachi SH big-endian COFF object, not stripped':'Hitachi',\
          'PDP-11 UNIX/RT ldp':'PDP-11',\
          'ISO-8859 text':'ISO-8859',\
          'ISO-8859 text, with no line terminators':'ISO-8859-NLT',\
          'ASCII text':'ASCII',\
          'ASCII text, with no line terminators':'ASCII-NLT',\
          'PDF document, version 1.4':'PDF-1.4',\
          'DOS executable (COM)':'DOSCOM',\
          'ASCII English text, with CRLF line terminators':'ASCII-E-CRLFLT',\
          'ASCII mail text, with CRLF line terminators':'ASCII-mail-CRLFLT', \
          'JPEG image data, JFIF standard 1.01':'JPEG-1.01',\
          'PCX ver. 2.5 image data':'PCX-v2.5-Imagedata',\
          'SysEx File - GreyMatter':'SysEx-GreyMatter',\
          'MS Windows icon resource - 2 icons, 3x, 4-colors':'MSW-2i-3x-4x',\
          'Zip archive data, at least v1.0 to extract':'Ziparc-v1.0',\
          'news or mail, ASCII text, with CRLF line terminators':'newsRmailASCII_CRLFLT' }
    arrayElementNum = 0
    array_ind = 0
    dont_start_yet = True
    is_first_file = True
    page = 0
    max_entries_per_page =30
    outdir = ''
    featuredir = ''

    regTestExp = \
         {'numFormats':153, 'numfiles':130, 'dirs':23, \
          'deletedFiles':0, 'unusedFiles':0, 'emptyFiles':11, 'bigFiles':5, \
          'image_filename':"charlie-work-usb-2009-12-11.aff", \
          'partition_offset':512, 'block_count':258559, 'first_block':0, \
          'last_block':258558, 'ftype':1, 'ftype_str':"ntfs", 'block_size':258559}

    def __init__(self,fn):
        import os.path,glob
        self.name = fn
        if os.path.isfile(fn):
            self.dname = fn
            self.files = set([os.path.basename(x) for x in glob.glob(os.path.join(fn,"*.txt"))])

        # Initialize the values of the dict elements
        for ind in range (0, (len(FiwalkReport.dict_array)-1)):
            FiwalkReport.dict_val[ind] = 0

    def open(self,fname,mode='r'):
        print("D = %s " % fname);

    # The format string as found in the fiwalk text output is very long.
    # So a shorter name for each format is maintained. It is actually the
    # "value" part of the bcfmtDict structure, which has the "full name"
    # the dictionary key.
    def bcGetShortNameForFmt(self, fmt_str):
        for x in self.dictFileFmtStatic:
            if fmt_str == x:
                return(self.dictFileFmtStatic[fmt_str])
        else:
            # Not found in the static array. So make up one
            # Trim the ttrailing space and replace special chars with "-"
            fmt_str = fmt_str.strip()
            newstr = fmt_str[0:3]+'_'+fmt_str[len(fmt_str) - 3:]
            
            # Replace any special character by a '-'
            newstr = re.sub('[^0-9a-zA-Z_]+', '-', newstr)

            return (newstr)

    # The File-format list is maintained dynamically and is populated as
    # a new file-format is read from the main dictionary.
    def bcAddToFmtList(self, fmt_str):
        self.numFormats += 1
        # Check if the fmt_str is not in the list already
        for x in self.bcFmtDict:
            shortForm = self.bcFmtDict[x]
            if fmt_str == x:
                ## print("D: FOUND fmt:%s, Incrementing Val to %d " \
                ## %(fmt_str,self.dictFileFmtVal[shortForm]))

                # Increment the frequency of this format for the bargraph
                self.dictFileFmtVal[shortForm] += 1
                break
        else:
            # This format is not found in the dict.
            # Look for this format string in the static array to get
            # the short string. If not found, make up one using the firs4t
            # 3 and last 3 characters. Then add the format to the dict.

            shortFmt = self.bcGetShortNameForFmt(self, fmt_str)

            # Add it to the dictionary.
            self.bcFmtDict[fmt_str] = shortFmt

            # Set the frequency of this format to 1 for the bargraph
            shortForm = self.bcFmtDict[fmt_str]
            self.dictFileFmtVal[shortForm] = 1

    #
    # Process the input when the input file is fiwalk's xml output
    #
    def process_generate_report_fiwalk_from_xml(self, fn):
        self.xmlInput = True
        input_file = fn.fiwalk_xmlfile
        FiwalkReport.outdir = fn.outdir

        # First get the partition information.
        bc_get_volume_info_from_sax(FiwalkReport, input_file, image_info, prtn_info_items, glb_image_info)

        # Now initialize the arrays that depend on the number of partitions.
        FiwalkReport.numfiles = [0] * FiwalkReport.numPartitions
        FiwalkReport.dirs = [0] * FiwalkReport.numPartitions
        FiwalkReport.deletedFiles = [0] * FiwalkReport.numPartitions
        FiwalkReport.unusedFiles = [0] * FiwalkReport.numPartitions
        FiwalkReport.moreNumlinks = [0] * FiwalkReport.numPartitions
        FiwalkReport.emptyFiles = [0] * FiwalkReport.numPartitions
        FiwalkReport.bigFiles = [0] * FiwalkReport.numPartitions

        # Process the xml file with sax
        bc_process_xmlfile_using_sax(FiwalkReport, input_file, prtn_info, glb_image_info, image_info)

        # Now generate the reports
        self.bc_generate_fiwalk_reports(fn)

        # Generate Excel report by default
        bc_generate_xlsx(fn)
        
        
    #
    # Process the input when the input file is fiwalk's text output
    #
    def process_generate_report_fiwalk_from_text(self, fn):
        self.xmlInput = False
        bc_process_textfile(fn, image_fileinfo, image_info, FiwalkReport)

    def bc_generate_fiwalk_reports(self, fn):
        # Output text file created using bulk-extractor output
        # We will use this text file to populate the pdf report
        ofn_be = fn.outdir + ".txt"
        FiwalkReport.outdir = fn.outdir
        prtn = FiwalkReport.numPartitions

        # Table headers
        header_be = ['Bulk Extractor Report Files','Feature Instances','FLTF','FUTF','FIER']
        header_files = ['Filename','Partition','DIR','Size','Deleted','Filetype']
        
        tab_header_delfiles = [' Partition ', 'Deleted File']
        tab_header_file_fmts = ['Partition', 'File']
        tab_header_statistics = ['Feature', 'Value']
        tab_header_bargraph = ['Format', 'Short Form', 'Files']

        # Data for Histogram
        # The frequency of each file-format type is mapped into a histogram/plot.
        # We calculate the number of files in each file format here.

        num_fmt_files = 0
        if (PdfReport.bc_max_fmtfiles_to_report):
            for x in self.bcFmtDict:
              file_format = x
              short_fmt_name = self.bcFmtDict[x]
              pdf=PDF()
              pdf.compress = False
              pdf.set_font('Arial','',10)
              pdf.add_page()
              pdf.make_table_fmtfiles(tab_header_file_fmts, file_format)
              pdf_file = fn.outdir + '/format_' + short_fmt_name + '.pdf'
                  
              pdf.output(pdf_file,'F')
              bc_utils.bc_addToReportFileList(pdf_file, PdfReport)
          
              num_fmt_files += 1
  
              # if the configured value for max fmtfiles is 0, it reports all.
              # else it uses the number specified in the config file.
              # If the number not configured, it uses the hardcoded default:20
              if PdfReport.bc_max_fmtfiles_to_report and \
                   num_fmt_files >= PdfReport.bc_max_fmtfiles_to_report:
                  ## print("D: FMT files exceeded max limit of %d" %(num_fmt_files))
                  break

        ## Report the bargraph only if the configuration file says so
        outfile = FiwalkReport.outdir + '/bc_format_bargraph.pdf'
        if PdfReport.bc_config_report_files['bc_format_bargraph']:
            bc_graph.bc_draw_histogram_fileformat(PdfReport, image_info, \
                                                  outfile, self.dictFileFmtVal)
  
            # Also make a table of the same information
            pdf=PDF()
            pdf.compress = False
            pdf.set_font('Arial','',10)
            pdf.add_page()
            pdf.bc_make_table_fileformat(tab_header_bargraph, \
                        self.dictFileFmtVal, self.bcFmtDict)
            pdf_file = fn.outdir + '/format_table.pdf'
            pdf.output(pdf_file,'F')
            bc_utils.bc_addToReportFileList(pdf_file, PdfReport)
  
  
        ## Report the Fiwalk Report file only if the config file says so
        if PdfReport.bc_config_report_files['FiwalkReport'] == 1:
            pdf=PDF()
            pdf.compress = False
            pdf.set_title("Bitcurator Report")
 
            # Print the statistics first
            pdf.set_font('Arial','',10)
            pdf.add_page()

            pdf.make_table_stat(tab_header_statistics)
  
            '''
            # If configured as -1, the table of files is not generated.
            if (PdfReport.bc_config_report_lines['FiwalkReport'] != -1):
                pdf.set_font('Arial','',10)
                pdf.add_page()
                pdf.make_table(header_files)
            '''
            pdf_file = fn.outdir + '/FiwalkReport.pdf'
            pdf.output(pdf_file,'F')
            bc_utils.bc_addToReportFileList(pdf_file, PdfReport)
          
        # Generate the Report of deleted files
  
        ## Report the Deleted Files only if the config file says so
        if PdfReport.bc_config_report_files['FiwalkDeletedFiles'] == 1:
            ## print("D: Generating Deleted Files Report")
            pdf=PDF()
            pdf.compress = False
            pdf.set_font('Arial','B',10)
            pdf.add_page()
            y = pdf.get_y()
            pdf.set_y(y+10)
            pdf.make_table_delfiles(tab_header_delfiles)
            pdf_file = fn.outdir + '/FiwalkDeletedFiles.pdf'
            print("Generating ", pdf_file)
            pdf.output(pdf_file, 'F')
            bc_utils.bc_addToReportFileList(pdf_file, PdfReport)
  
        ## Now add the info from bulk-extractor output (be_ofn)
        ## Report the BE Report file only if the config file says so
        if PdfReport.bc_config_report_files['BeReport'] == 1:
              pdf=PDF_BE()
              pdf.compress = False
  
              pdf.set_font('Arial','B',10)
              pdf.add_page()
              y = pdf.get_y()
              pdf.set_y(y+10)
              pdf.set_text_color(128)
              pdf.make_table_be(header_be, ofn_be)
  
              pdf_file = fn.outdir + '/BeReport.pdf'
              pdf.output(pdf_file,'F')
              bc_utils.bc_addToReportFileList(pdf_file, PdfReport)

        ## print("Printing the Generated PDF files ")
        bc_utils.bc_printReportFileList(PdfReport, FiwalkReport)


if __name__=="__main__":
    import sys, time, re

    parser = ArgumentParser(prog='generate_report.py', description='Generate Reports from "bulk_extractor" and "fiwalk" outputs')
    parser.add_argument('--regress', action='store_true', help='Regression')
    ###parser.add_argument('--fiwalk_txtfile', action='store', help="Use fiwalk-generated text file ")
    parser.add_argument('--fiwalk_xmlfile', action='store', help="Use fiwalk-generated XML file ")
    ##parser.add_argument('--xlsx', action='store_true', help="output XLS file ")
    parser.add_argument('--annotated_dir', action='store', help="Directory containing annotated files ")
    parser.add_argument('--outdir',action='store',help='Output directory; must not exist')
    ###parser.add_argument('--gui',action='store_true',help='Use GUI')

    args = parser.parse_args()

    ## print("D: PDF REPORT", args.pdf_report)
    ## print("D: FIWALK_XMLFILE", args.fiwalk_xmlfile)
    ## print("D: Annotated_DIR", args.annotated_dir)
    ## print("D: OUTDIR", args.outdir)
    ## print("D: XLS file", args.xls)

    ## print("DIR: ", os.path.dirname(args.fiwalk_xmlfile))
    
    config_file = "/etc/bitcurator/bc_report_config.txt"
    if args.regress:
        print("\n >> Regression test not supported at this time \n ")
        exit(1)

        # FIXME: Fix the regression test
        use_config_file = (input (">>> Do you want to specify the" \
                                   "configuration file?: [Y/N]:"))

        if use_config_file == 'Y' or use_config_file == 'y':
            config_file = (input (">>> Please specify the configuration" \
                          " file[/etc/bitcurator/bc_report_config.txt]: "))

            # If hit return, use the default: bc_report_config.txt.
            # In either case, see if the file exists.
            if (config_file == ''):
                # User pressed return. Use the default file: bc_report_config.txt
                if (os.path.exists("./bc_report_config.txt")):
                    config_file = "./bc_report_config.txt"
                else: 
                    print(">>> Using the configuration file /etc/bitcurator/bc_report_config.txt")
                    config_file = "/etc/bitcurator/bc_report_config.txt"

            if not os.path.exists(config_file):
                print(">>> Configuration file %s does not exist. Using default values" %(config_file))
                use_config_file = "N"

        elif use_config_file == 'N' or use_config_file == 'n':
            print(">>> You have opted to select the default values for reporting")
        else:
            print(">>> Wrong option. Defaulting")
            use_config_file = 'N'
        
        fiwalk_txtfile = None
        args.pdf_report = True
        fiwalk_xmlfile = "xmlfile" # Just some string. It will get overwritten
        
        report_fi = FiwalkReport(fiwalk_xmlfile)
        bc_config.bc_get_regtest_parameters(FiwalkReport, config_file)

        # We are not running any regression test on xlsx yet.
        fiwalk_xlsx = None

        args.annotated_dir = FiwalkReport.regress_annotated_dir
        args.fiwalk_xmlfile = FiwalkReport.regress_input_xml_file
        args.outdir = FiwalkReport.regress_outdir

        report = PdfReport(FiwalkReport.regress_annotated_dir, \
                           FiwalkReport.regress_outdir, \
                           use_config_file, config_file)
        report.be_process_generate_report(args, use_config_file)

        report_fi.process_generate_report_fiwalk_from_xml(args)

        # Test the results
        print("\n Starting the regression test: \n")
        bc_regress.reg_test(FiwalkReport, image_info, args.outdir)

    else:

        use_config_file = (input (">>> Do you want to specify the" \
                                  " configuration file?: [Y/N]:"))

        if use_config_file == 'Y' or use_config_file == 'y':
            config_file = (input (">>> Please specify the configuration"
                           " file[/etc/bitcurator/bc_report_config.txt]: "))

            # If hit return, use the default: bc_report_config.txt.
            # In either case, see if the file exists.
            if (config_file == ''):
                # User pressed return. Use the default file: bc_report_config.txt
                if (os.path.exists("./bc_report_config.txt")):
                    config_file = "./bc_report_config.txt"
                else: 
                    print(">>> Using the configuration file /etc/bitcurator/bc_report_config.txt")
                    config_file = "/etc/bitcurator/bc_report_config.txt"

            if not os.path.exists(config_file):
                print(">>> Configuration file %s does not exist. "\
                      "Using default values" %(config_file))
                use_config_file = "N"
                
        elif use_config_file == 'N' or use_config_file == 'n':
            print(">>> You have opted to select the default values for reporting")
        else:
            print(">>> Wrong option. Defaulting")
            use_config_file = 'N'

        report = PdfReport(args.annotated_dir, args.outdir, use_config_file, config_file)
        report.be_process_generate_report(args, use_config_file)

        # Using the xml file generated by fiwalk, report the following
        # information:

        fiwalk_txtfile = None
        fiwalk_xmlfile = None
        fiwalk_xlsx = True  # By default, xlsx files are generated
        
        if args.fiwalk_xmlfile:
            fiwalk_xmlfile = args.fiwalk_xmlfile

            ## print("D: Using Fiwalk XML file ", fiwalk_xmlfile)

            report_fi = FiwalkReport(args.fiwalk_xmlfile)
            report_fi.process_generate_report_fiwalk_from_xml(args)


        exit(1)
