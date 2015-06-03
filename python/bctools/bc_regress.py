#!/usr/bin/python
# coding=UTF-8
#
# BitCurator
# 
# This code is distributed under the terms of the GNU General Public 
# License, Version 3. See the text file "COPYING" for further details 
# about the terms of this license.
#
# This is a python file containing some regression test routines for
# generate_reports 

import bc_utils
import os, filecmp


def reg_fiwalk_metadata_test(FiwalkReport, image_info):

    # Check the technical metadata values

    ## print("D: IMAGEINFO:", image_info)
    ## print("D: EXPECTED: ", FiwalkReport.regTestExp)

    if (image_info['ftype_str'] == \
                    FiwalkReport.regTestExp['ftype_str'].strip() and
        image_info['ftype'] == str(FiwalkReport.regTestExp['ftype']) and
        image_info['partition_offset'] == \
          str(FiwalkReport.regTestExp['partition_offset']) and 
        image_info['block_size'] == str(FiwalkReport.regTestExp['block_size']) and
        image_info['first_block'] == \
                    str(FiwalkReport.regTestExp['first_block']) and
        image_info['last_block'] == str(FiwalkReport.regTestExp['last_block']) and
        image_info['block_count'] == \
                    str(FiwalkReport.regTestExp['block_count']) and
        bc_utils.filename_from_path(image_info['image_filename']) == \
                    str(FiwalkReport.regTestExp['image_filename']) and
        FiwalkReport.dirs == FiwalkReport.regTestExp['dirs'] and
        FiwalkReport.emptyFiles == FiwalkReport.regTestExp['emptyFiles'] and
        FiwalkReport.unusedFiles == FiwalkReport.regTestExp['unusedFiles'] and
        FiwalkReport.numfiles == FiwalkReport.regTestExp['numfiles'] and
        FiwalkReport.bigFiles == FiwalkReport.regTestExp['bigFiles'] and
        FiwalkReport.deletedFiles == FiwalkReport.regTestExp['deletedFiles']):
 
        print("FIWALK METADATA TEST: 		PASS")
    else:
        print("FIWALK METADATA TEST: 		FAIL")
        print("Read: ftype_str: %s, Expected: %s " %(image_info['ftype_str'],
                  FiwalkReport.regTestExp['ftype_str'].strip()))
        print("Read: ftype:%s, Expected:%s " %(image_info['ftype'], 
                  FiwalkReport.regTestExp['ftype']))
        print("Read: partition_offset:%s, Expected:%s " \
                %(image_info['partition_offset'], 
                  FiwalkReport.regTestExp['partition_offset']))
        print("Read: block_size:%s, Expected:%s " %(image_info['block_size'], 
                  FiwalkReport.regTestExp['block_size']))
        print("Read: first_block:%s, Expected:%s " %(image_info['first_block'], 
                  FiwalkReport.regTestExp['first_block']))
        print("Read: last_block:%s, Expected:%s " %(image_info['last_block'], 
                  FiwalkReport.regTestExp['last_block']))
        print("Read: block_count:%s, Expected:%s " %(image_info['block_count'], 
                  FiwalkReport.regTestExp['block_count']))
        print("Read: dirs:%s, Expected:%s " %(FiwalkReport.dirs, 
                  FiwalkReport.regTestExp['dirs']))
        print("Read: emptyFiles:%s, Expected:%s " %(FiwalkReport.emptyFiles, 
                  FiwalkReport.regTestExp['emptyFiles']))
        print("Read: unusedFiles:%s, Expected:%s " %(FiwalkReport.unusedFiles, 
                  FiwalkReport.regTestExp['unusedFiles']))
        print("Read: numfiles:%s, Expected:%s " %(FiwalkReport.numfiles, 
                  FiwalkReport.regTestExp['numfiles']))
        print("Read: bigFiles:%s, Expected:%s " %(FiwalkReport.bigFiles, 
                  FiwalkReport.regTestExp['bigFiles']))
        print("Read: deletedFiles:%s, Expected:%s " %(FiwalkReport.deletedFiles, 
                  FiwalkReport.regTestExp['deletedFiles']))

def reg_be_statistics(reg_beinfo_file, outdir):
    # check if the file-to-compare exists or not.
    if not os.path.exists(reg_beinfo_file):
        print("File %s does not exist" %reg_beinfo_file)
        print("BULK EXTRACTOR STASTISTICS TEST:FAIL")
        return
    
    # Now compare the generated file outdir.txt and temporarily
    # generated file outdir.txt which contains the end-of-file parameters
    # that the anotated reports report.
    out_stats_file = outdir + ".txt"
    if filecmp.cmp(out_stats_file, reg_beinfo_file) == True:
        print("BULK EXTRATOR STASTISTICS TEST:	PASS")
    else:
        print("BULK EXTRACTOR STASTISTICS TEST:	FAIL")
  
# bc_max_fmtfiles_to_report is set to 20 for regression test. The following
# is an expected value list for the frequency for 1st 20 formats for the 
# regression test image.
regressFmtListCharlie =  {'dat_ata': 31, 'new_ors': 1, 'PCX_ata': 1, \
    'PDF_1-4': 6, 'MS-_ors': 1, 'x86_x0-': 1, 'Sys_ter': 1, 'emp_ct-': 2, \
    'TIF_ian': 2, 'ASC_xt-': 1, 'JPE_-01': 4, 'PE3_ive': 1, 'JPE_61-': 2, \
    'ASC_ors': 40, 'Com_nfo': 1, 'emp_pty': 9, 'ASC_ct-': 1}

def reg_fiwalk_fmt_freq_test(FiwalkReport):
    if (FiwalkReport.dictFileFmtVal == regressFmtListCharlie):
        print("FIWALK FORMAT FREQUENCY TEST: 	PASS")
    else:  
        print("FIWALK FORMAT FREQUENCY TEST: 	FAIL")
    
def reg_fiwalk_format_test(FiwalkReport):
    # check the number of format files generated
    if (FiwalkReport.numFormats == FiwalkReport.regTestExp['numFormats']):
        print("FIWALK FORMAT TEST: 		PASS")
    else:
        print("FIWALK FORMAT TEST: 		FAIL")

def reg_test(FiwalkReport, image_info, outdir):
    FiwalkReport.regressionTest = True
    reg_fiwalk_metadata_test(FiwalkReport, image_info)
    reg_be_statistics(FiwalkReport.regress_beinfo_file, outdir)
    reg_fiwalk_format_test(FiwalkReport)
    reg_fiwalk_fmt_freq_test(FiwalkReport)


