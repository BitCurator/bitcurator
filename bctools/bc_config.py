#!/usr/bin/python
# coding=UTF-8
#
# BitCurator 
# 
# This code is distributed under the terms of the GNU General Public 
# License, Version 3. See the text file "COPYING" for further details 
# about the terms of this license.
#
# This module contains read and write routines related to the 
# configuration information used by BitCurator - in particular the 
# generate_reports script

import os, sys
from configobj import ConfigObj
import re
#import bc_utils,re

def bc_parse_config_file(PdfReport, FiwalkReport, config_file):

    print(config_file)

    # Open the configuration file as a ConfigObj
    config = ConfigObj(config_file)
    
    # Clone the static dictionary of file formats.
    # Limit the number by setting S:MAX_FILE_FORMAT_FILES_TO_REPORT:20
    PdfReport.bc_config_filefmt_files = FiwalkReport.dictFileFmtStatic.copy()

    # Initialize all the values to 0
    for x, y in PdfReport.bc_config_filefmt_files.items():
        PdfReport.bc_config_filefmt_files[x] = 0

    # By default, report special files
    PdfReport.bc_config_report_special_files = True
    # print("D:config_filefmt: ", PdfReport.bc_config_filefmt_files)

    # Logo section: Set logo filename and properties (L)
    #logo_sec = config['logo_section']
    #for key in logo_sec:
    #   if key == 'filepath':
    #      logo_filepath = logo_sec['filepath']
    #   else:
    #      logo_filepath = 'empty'
    # Overwrite the logo path:
    #if logo_filepath != 'empty':
    #   PdfReport.logo = logo_filepath   
 
    # Feature section: Set feature report output parameters (F)
    feature_sec = config['feature_section']
    for key in feature_sec:
       #print(key, feature_sec[key])
       if key in PdfReport.bc_config_feature:
          #Enable the report and set number of lines to output for each feature (0 = all)
          PdfReport.bc_config_feature[key] = 1
          PdfReport.bc_config_feature_lines[key] = int(feature_sec[key])

    # Report section: Set properties for individual reports (R)
    report_sec = config['report_section']
    for key in report_sec:
       #print(key, report_sec[key])
       if key in PdfReport.bc_config_report_files:
          PdfReport.bc_config_report_files[key] = 1   
          PdfReport.bc_config_report_lines[key] = int(report_sec[key])
       else:
          print("Info: Report file %s is not currently managed" % key)
          print("Info: Fix the config file")
 
    # Miscellaneous flags: Control other features (S)
    misc_sec = config['misc_section']
    for key in misc_sec:
       #print(key, misc_sec[key])
       if key == 'REPORT_SPECIAL_FILES':
          if misc_sec[key] == 'YES':
             PdfReport.bc_config_report_special_files = True
          else:
             # print("D: Not reporting Special files")
             PdfReport.bc_config_report_special_files = False
       elif key == 'MAX_LINES_TO_REPORT':
          PdfReport.bc_max_lines_to_report = int(misc_sec[key])
       elif key == 'MAX_FILE_FORMAT_FILES_TO_REPORT':
          PdfReport.bc_max_fmtfiles_to_report = int(misc_sec[key])
       elif key == 'MAX_FEATURE_FILES_TO_REPORT':
          PdfReport.bc_max_featfiles_to_report = int(misc_sec[key])
       elif key == 'MAX_FORMATS_FOR_BAR_GRAPH':
          PdfReport.bc_max_formats_in_bar_graph = int(misc_sec[key])
       elif key == 'FEATURE_OUTPUTS_IN_PDF':
          PdfReport.bc_feature_output_in_pdf = int(misc_sec[key])

    # Regression flags: Control other features (S)
    regress_sec = config['regress_section']
    for key in regress_sec:
       #print(key, regress_sec[key])
       # Regression test parameters
       if key == 'REGRESS_ANNOTATED_DIR':
          PdfReport.bc_regr_annotated_dir = regress_sec[key]
       elif key == 'REGRESS_INPUT_XML_FILE':
          PdfReport.bc_regr_xml_file = regress_sec[key]
       elif key == 'REGRESS_OUTDIR':
          PdfReport.bc_regr_xml_file = regress_sec[key]

    # For regression test we keep the max formats to be reported to 20
    if FiwalkReport.regressionTest == True:
       PdfReport.bc_max_fmtfiles_to_report = 20

def bc_write_config_file(config_file):

    # Set up the configuration object
    config = ConfigObj()
    # Set the filename
    config.filename = config_file

    # Build initial comment
    config.initial_comment = [
      '#',
      '# Configuration file for BitCurator Reporting',
      '# logo_section: Sets up the logo parameters',
      '# feature_section: Sets number of lines reported for features',
      '# report_section: Sets parameters for fiwalk/bulk_extractor reports',
      '# misc_section: Special flags for other output',
      '#'
    ]
    
    # Set up the logo section
    #config['logo_section'] = {}
    logo_section = {
    # Enter a filepath here if you wish to overwrite the default logo
    #'filepath': '/home/bcadmin/logos/FinalBitCuratorLogo-NoText.png',
    'empty' : 'empty'
    }
    config['logo_section'] = logo_section

    # Set up the feature section
    feature_section = {
    'aes_keys' : 0,
    'alerts' : 0,
    'ccn_track2' : 0,
    'ccn' : 0,
    'domain' : 0,
    'elf' : 0,
    'email' : 0,
    'ether' : 0,
    'exif' : 0,
    'find' : 0,
    'gps' : 0,
    'hex' : 0,
    'ip' : 0,
    'jpeg_carved' : 0,
    'json' : 0,
    'kml' : 0,
    'pii' : 0,
    'rar' : 0,
    'rfc822' : 0,
    'telephone' : 0,
    'unrar_carved' : 0,
    'unzip_carved' : 0,
    'url' : 0,
    'vcard' : 0,
    'windirs' : 0,
    'winpe' : 0,
    'winprefetch' : 0,
    'zip' : 0
    }
    config['feature_section'] = feature_section

    # Set up the report section
    report_section = {
    'bc_format_bargraph' : 0, 
    'fiwalk_report' : -1,
    'fiwalk_deleted_files' : 0,
    'bulk_extractor_report' : 0
    }
    config['report_section'] = report_section
    
    # Set up other misc options
    misc_section = {
    'REPORT_SPECIAL_FILES' : 'YES',
    'MAX_LINES_TO_REPORT' : 1000,
    'MAX_FILE_FORMAT_FILES_TO_REPORT' : 0,
    'MAX_FEATURE_FILES_TO_REPORT' : 50,
    'FEATURE_OUTPUTS_IN_PDF' : 0
    }
    config['misc_section'] = misc_section

    # Set up the regression section
    regress_section = {
    'REGRESS_ANNOTATED_DIR' : './bc_regress_dir/regress_annotated_charlie_output',
    'REGRESS_INPUT_XML_FILE': './bc_regress_dir/regress_charlie_fi_F.xml',
    'REGRESS_OUTDIR': './bc_regress_dir/regress_outdir',
    'REGRESS_BEINFO_FILE' : './bc_regress_dir/regress_charlie_beinfo.txt'
    }
    config['regress_section'] = regress_section

    # Write out the comment
    config.comments = {'logo_section': ['', '#', '# Set up the logo section', '#'],
    'feature_section': ['', '#', '# Set up the feature section', '#'],
    'report_section': ['', '#', '# Set up the report section', '#'],
    'misc_section': ['', '#', '# Set up the misc section', '#'],
    'regress_section': ['', '#', '# Set up the regression section', '#']
    }

    # Write out the configuration file
    config.write()

# Uncomment for testing only
# Main application
#if __name__ == "__main__":
#    bc_write_config_file("/home/bcadmin/Desktop/bc_report_config.txt")
#    #bc_parse_config_file(0, 0, "/home/bcadmin/Desktop/bc_report_config.txt")

