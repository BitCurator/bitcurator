#!/usr/bin/env python
#
# BitCurator
# 
# This code is distributed under the terms of the GNU General Public 
# License, Version 3. See the text file "COPYING" for further details 
# about the terms of this license.
#
# Generate report from a fiwalk DFXML file 
# 

import sys,os,shelve
import re,dfxml,fiwalk
#from generate_report import glb_image_info

t_image_info = {'partition_offset':0,'block_count':0, 'first_block':0,'last_block':0, 'block_size':0, 'ftype':0,'ftype_str':0 }

def bc_get_volume_info_from_sax(FiwalkReport, fn, image_info, prtn_info_items, glb_image_info):

    #
    # Callback function to process the SAX stream for volume object
    #
    def cbv(fv):
        t_image_info['partition_offset'] = fv.partition_offset()
        t_image_info['block_count'] = fv.block_count()
        t_image_info['last_block'] = fv.last_block()
        t_image_info['first_block'] = fv.first_block()
        t_image_info['block_size'] = fv.block_count()
        t_image_info['ftype'] = fv.ftype()
        t_image_info['ftype_str'] = fv.ftype_str()

        FiwalkReport.numPartitions +=1;

        glb_image_info.append({
                  prtn_info_items[0]:t_image_info['partition_offset'],\
                  prtn_info_items[1]:t_image_info['block_count'], \
                  prtn_info_items[2]:t_image_info['first_block'], \
                  prtn_info_items[3]:t_image_info['last_block'], \
                  prtn_info_items[4]:t_image_info['block_size'], \
                  prtn_info_items[5]:t_image_info['ftype'],  \
                  prtn_info_items[6]:t_image_info['ftype_str']}) 

    xmlfile = open(fn, 'rb')

    '''
    ## NOTE: Originally we mandated the xml file to end with .xml
    ## Code retained for reference and context
    # Currently we support taking only xml file as input. The following
    # check is for future enhancement.
    if fn.endswith('xml'):
        r = fiwalk.fiwalk_vobj_using_sax(xmlfile=open(fn, 'rb'),callback=cbv)
        image_info['image_filename'] = r.imageobject._tags['image_filename']
        image_info['partitions'] = str(FiwalkReport.numPartitions)
      
    else:
        # We use this call if we're processing a disk image
        print("Warning: Expected an XML File ")
    '''
    r = fiwalk.fiwalk_vobj_using_sax(xmlfile=open(fn, 'rb'),callback=cbv)
    image_info['image_filename'] = r.imageobject._tags['image_filename']
    image_info['partitions'] = str(FiwalkReport.numPartitions)

#
# From dfxml utilities, Get the file and volume objects extracted 
# from the xml file created by fiwalk. In the call-back routine,
# populate the array of dictionaries, fiwalkDictList, using the
# objects.  
#
def bc_process_xmlfile_using_sax(FiwalkReport, fn, prtn_info, glb_image_info, image_info):

    '''
    #
    # Callback function to process the SAX stream for volume object
    #
    def cbv(fv):
        prtn_info['partition_offset'] = fv.partition_offset()
        prtn_info['block_count'] = fv.block_count()
        prtn_info['last_block'] = fv.last_block()
        prtn_info['first_block'] = fv.first_block()
        prtn_info['block_size'] = fv.block_count()
        prtn_info['ftype'] = fv.ftype()
        prtn_info['ftype_str'] = fv.ftype_str()

        # glb_image_info.append(prtn_info)
        # NOTE: The above will overwrite the list with the new element as
        # every list element! Dumb!

        glb_image_info.append({prtn_info['partition_offset'], \
            prtn_info['block_count'], prtn_info['last_block'], \
            prtn_info['first_block'],  prtn_info['block_size'], \
            prtn_info['ftype'],  prtn_info['ftype_str']}) 
        ## print("DEBUG:", glb_image_info)
        ## print("DEBUG: VolumeObject:", fv)    
        ## print("DEBUG: Image Fileinfo: ", prtn_info)
    '''

    #
    # Callback function to process the SAX stream for file object
    #
    def cb(fi):
        # Form a list of dictionaries of the file attributes from the
        # xml file. Each dictionary represents one file (FiwalkReport.fiDictList)

        bc_make_dict(fi, FiwalkReport, fn)

    xmlfile = open(fn, 'rb')

    # We assume that we are processing a fiwalk XML fle
    fiwalk.fiwalk_using_sax(xmlfile=open(fn, 'rb'),callback=cb)

    ''' 
    ## NOTE: Original code preserved for reference and context. It was
    ## originally assumed that the xml file will have a .xml prefix.
    #
    # Currently we support taking only xml file as input. The following
    # check is for future enhancement.
    if fn.endswith('xml'):
        # We use this call if we're processing a fiwalk XML fle
        fiwalk.fiwalk_using_sax(xmlfile=open(fn, 'rb'),callback=cb)
    else:
        # We use this call if we're processing a disk image
        fiwalk.fiwalk_using_sax(imagefile=open(fn, 'rb'),callback=cb)
    '''

#
# bc_make_dict forms a list of dictionaries, where information from each 
# file object is put in a dictionary and the list has each of these
# dictionaries as its elements.
#
def bc_make_dict(fi, FiwalkReport, fn):
    FiwalkReport.array_ind += 1

    # Populate the bc_dict with the info from fi
    prtn = int(fi.partition()) - 1

    # Debug
    ## if (FiwalkReport.prevPartition != fi.partition()):
          ## Time for a new report
          ##print("Partition Change")
    # FiwalkReport.prevPartition = fi.partition()

    for i in FiwalkReport.dict_array:
        FiwalkReport.dict_val[i] = 0

    # Save the file attributes per partition
    FiwalkReport.dict_val["filename"] = fi.filename()
    FiwalkReport.dict_val['partition'] = fi.partition()
    if fi.is_dir():
        FiwalkReport.dict_val['name_type'] = 'd' 
        FiwalkReport.dirs[prtn] += 1
    elif fi.is_file():
        FiwalkReport.dict_val['name_type'] = 'r' 
        FiwalkReport.numfiles[prtn] += 1
    else:
        FiwalkReport.dict_val['name_type'] = 'x' 
    
    FiwalkReport.dict_val['filesize'] = str(fi.filesize())

    FiwalkReport.dict_val["alloc"] = False
    FiwalkReport.dict_val["unalloc"] = False

    if (fi.allocated()):
        FiwalkReport.dict_val["alloc"] = True
    else:
        FiwalkReport.dict_val["unalloc"] = True
        FiwalkReport.deletedFiles[prtn] += 1

    # If the XML file doesn't have the format information, we cannot
    # generate reports related to formats.
    if (fi.libmagic() == None):
        FiwalkReport.noLibMagic = True

    if FiwalkReport.noLibMagic == False:
        # If not alrady present in format array, add the fileformat
        FiwalkReport.dict_val['libmagic'] = fi.libmagic()
        FiwalkReport.bcAddToFmtList(FiwalkReport, fi.libmagic())

    # empty files and big files
    if fi.filesize() == 0:
        FiwalkReport.emptyFiles[prtn] += 1
    if fi.filesize() > 1024*1024:
        FiwalkReport.bigFiles[prtn] += 1

    # Now append this dictionary to the array FiwalkReport.fiDictList
    # which is an array of dictionaries.
    FiwalkReport.fiDictList.append({FiwalkReport.dict_array[0]:FiwalkReport.dict_val['filename'], \
         FiwalkReport.dict_array[1]:FiwalkReport.dict_val['partition'],\
         FiwalkReport.dict_array[2]:FiwalkReport.dict_val['id'],\
         FiwalkReport.dict_array[3]:FiwalkReport.dict_val['name_type'],\
         FiwalkReport.dict_array[4]:FiwalkReport.dict_val['filesize'],\
         FiwalkReport.dict_array[5]:FiwalkReport.dict_val['alloc'],\
         FiwalkReport.dict_array[6]:FiwalkReport.dict_val['unalloc'],\
         FiwalkReport.dict_array[7]:FiwalkReport.dict_val['used'],\
         FiwalkReport.dict_array[8]:FiwalkReport.dict_val['inode'],\
         FiwalkReport.dict_array[9]:FiwalkReport.dict_val['meta_type'],\
         FiwalkReport.dict_array[10]:FiwalkReport.dict_val['mode'],\
         FiwalkReport.dict_array[11]:0,\
         FiwalkReport.dict_array[12]:FiwalkReport.dict_val['uid'],\
         FiwalkReport.dict_array[13]:FiwalkReport.dict_val['gid'],\
         FiwalkReport.dict_array[14]:FiwalkReport.dict_val['mtime'],\
         FiwalkReport.dict_array[15]:FiwalkReport.dict_val['mtime_txt'],\
         FiwalkReport.dict_array[16]:FiwalkReport.dict_val['ctime'],\
         FiwalkReport.dict_array[17]:FiwalkReport.dict_val['ctime_txt'],\
         FiwalkReport.dict_array[18]:FiwalkReport.dict_val['atime'],\
         FiwalkReport.dict_array[19]:FiwalkReport.dict_val['atime_txt'],\
         FiwalkReport.dict_array[20]:FiwalkReport.dict_val['crtime'],\
         FiwalkReport.dict_array[21]:FiwalkReport.dict_val['crtime_txt'],\
         FiwalkReport.dict_array[22]:FiwalkReport.dict_val['libmagic']})

def bc_print_fileobj(fi):
    print("Found a regular file or directory: ")
    print("Partition: " + fi.partition())
    print("Filename: " + fi.filename())
    print("Filesize: ", fi.filesize())
    print("UID: ", fi.uid())
    print("GID: ", fi.gid())
    print("Meta type: ", fi.meta_type())
    print("Mode: ", fi.mode())
    print("Change time: ", fi.ctime())
    print("Access time: ", fi.atime())
    print("Create time: ", fi.crtime())
    print("Modification time: ", fi.mtime())
    print("SHA1 Hash: ", fi.sha1())
    print("MD5 Hash: ", fi.md5())
    print("Direc: ", fi.md5())
    print("MD5 Hash: ", fi.md5())
 
