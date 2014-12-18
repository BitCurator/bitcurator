#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# BitCurator
#
# This code is distributed under the terms of the GNU General Public
# License, Version 3. See the text file "COPYING" for further details
# about the terms of this license.
#
# bc_premis_genxml.py
#
# Generate XML tree for premis events
#

import os, fiwalk, uuid, sys
import lxml.builder as lb
from lxml import etree
try:
    from argparse import ArgumentParser
except ImportError:
    raise ImportError("This script requires ArgumentParser which is in Python 2.7 or Python 3.0")

global root
root = "null"

class BcPremisFile:

    # The first block of disk-image object 
    def bcPremisGenXmlObject(self, image_name):
        global root
        object1 = etree.SubElement(root, 'object')
        root.append(object1)

        originalName = etree.SubElement(object1, "originalName")
        originalName.text = image_name
        object1.append(originalName)

        objectIdentifier = etree.SubElement(object1, "objectIdentifier")
        object1.append(objectIdentifier)

        objectIdentifierType = etree.Element('objectIdentifierType')
        #objectIdentifierType.text = image_name
        objectIdentifierType.text = "UUID"
        objectIdentifier.append(objectIdentifierType)

        objectIdentifierValue = etree.Element('objectIdentifierValue')
        objectIdentifierValue.text = str(uuid.uuid1())
        objectIdentifier.append(objectIdentifierValue)

    # Extract the image_name from the dfxml line "command_line"
    def extractImageName(self, dfxml_command_line, dfxml_type):
        # Command_line text looks like this for fiwalk dfxml:
        # <command_line>fiwalk -f -X <pathToXml> <pathToImage>.aff</command_line>
        # it looks like the following for BE reports dfxml:
        # <command_line>cmd/bulk_extractor <image>.aff -o <path_to_eDir></command_line>
        templist = dfxml_command_line.split(" ")
        if (dfxml_type == "fw"):
            # print("D: command_line as list: ", templist[4])
            return templist[4]
        elif dfxml_type == "be":
            # print("D: command_line as list: ", templist[2] )
            return templist[2]

    def bcGenPremisEvent(self, root, eIdType, eType, eDetail, eDateTime, eOutcome, eoDetail, of_premis, write_to_file = False):
        # Generate the Event:
        event = etree.SubElement(root, 'event')
        root.append(event)
        eventIdentifier = etree.SubElement(event, "eventIdentifier")
        event.append(eventIdentifier)

        eventIdentifierType = etree.SubElement(eventIdentifier, "eventIdentifierType")
        # Use UUID generation if eIDType is set to 0
        #if (eIdType == 0):
        eventIdentifierType.text = "UUID"
        #else:
        #    eventIdentifierType.text = str(eIdType)

        eventIdentifier.append(eventIdentifierType)
     
        eventIdentifierValue = etree.SubElement(eventIdentifier, "eventIdentifierValue")
        #eventIdentifierValue.text = eIdVal
        eventIdentifierValue.text = str(uuid.uuid1())
        eventIdentifier.append(eventIdentifierValue)

        eventType = etree.SubElement(event, "eventType")
        eventType.text = eType
        event.append(eventType)

        eventDetail = etree.SubElement(event, "eventDetail")
        eventDetail.text = eDetail
        event.append(eventDetail)

        eventDateTime = etree.SubElement(event, "eventDateTime")
        eventDateTime.text = eDateTime

        event.append(eventDateTime)
        eventOutcomeInformation = etree.SubElement(event, "eventOutcomeInformation")
        event.append(eventOutcomeInformation)

        eventOutcome = etree.SubElement(eventOutcomeInformation, "eventOutcome")
        eventOutcome.text = eOutcome
        eventOutcomeInformation.append(eventOutcome)

        eventOutcomeDetail = etree.SubElement(eventOutcomeInformation, "eventOutcomeDetail")
        eventOutcomeDetail.text = eoDetail
        eventOutcomeInformation.append(eventOutcomeDetail)

        # pretty string: 
        s = etree.tounicode(root, pretty_print=True)
        
        #print(s)
        if (write_to_file == True):
            of_premis.write(bytes(s, 'UTF-8'))
 
    # Generate Object and event parts for the disk image
    def bcGenPremisXmlDiskImage(self, image_name, premis_image_info, premis_file):
        # We will not create the output file till the last event.
        of_premis = "null"

        # create XML 
        global root
        root = etree.Element("premis", xmlns="info:lc/xmlns/premis-v2", xsi="info:lc/xmlns/premis-v2 http://www.loc.gov/standards/premis/v2/premis-v2-1.xsd", version="2.1")
        
        # Generate the disk image Object segment 
        self.bcPremisGenXmlObject(image_name)

        # Generate the disk image event segment
        eventIdType = 0  # UUID
        #if image_name.endswith(".aff"):
        #    eventIdVal = "affinfo "+image_name
        #elif image_name.endswith(".E01"):
        #    eventIdVal = "E01"+image_name
        #else:
        #    eventIdVal = image_name

        eventType = "Capture"

        # Display image path and name as eventDetail
        eventDetail = image_name

        eDateTime = premis_image_info['acq_date']
        eoDetail = 'Version: '+ str(premis_image_info['version']) + ', Image size: '+ str(premis_image_info['imagesize'])
        if image_name.endswith(".aff"):
            eOutcome = "AFF"
        elif image_name.endswith(".E01"):
            eOutcome = "E01"
        else:
            eOutcome = "Unknown image type"
            print(">> No Premis Events generated: ", eOutcome)
            return(" ")

        ## print("D: Geenrating disk image Event: ", root, image_name)

        self.bcGenPremisEvent(root, eventIdType, eventType, eventDetail, eDateTime, eOutcome, eoDetail, of_premis, False)
        return root

    # Generate premis XML code for Fiwalk event
    def bcGenPremisXmlFiwalk(self, dfxmlfile, premis_file, outcome=True, fw_tab=False):
    
        # If dfxmlfile doesn't exist, Fiwalk command probably failed.
        # If outcome is False, it is confirmed to have failed.
        # Generate premis event accordingly.
        # FIXME: Add premis event for failed case here.

        # We don't write to the file till the last event is done. If this
        # routine is invoked by a Fiwalk-tab, this is the last event.
        # For such a case, create a new file.

        ## print("D: bcGenPremisXmlFiwalk: XmlFile: ", dfxmlfile)
        ## print("D: bcGenPremisXmlFiwalk: Premis file: ", premis_file)
        if fw_tab == True:
          if os.path.exists(premis_file):
            of_premis = open(premis_file,"wb")
            line1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            of_premis.write(bytes(line1, 'UTF-8'))
          else:
            of_premis = "null"
        else:
            of_premis = "premis_file"

        # Get the image name from "command_line" part of dfxml file:
        dfxml_command_line = fiwalk.fiwalk_xml_command_line(dfxmlfile)
        image_name = self.extractImageName(dfxml_command_line, "fw")
        
        # Generate the Fiwalk Event:
        eventIdType = 0  # UUID

        #eventIdVal = dfxml_command_line
        eventDetail = dfxml_command_line

        eDateTime = fiwalk.fiwalk_xml_start_time(dfxmlfile)
        eoDetail = "Produced DFXML file: " + dfxmlfile
        if (outcome == True):
            eOutcome = "Completed" 
        else:
            eOutcome = "Failed" 

        ## print("D:bcGenPremisXmlFiwalk: Generating Premis Event: ", root, dfxmlfile)

        if of_premis != "null":
           self.bcGenPremisEvent(root, eventIdType, "File System Analysis", eventDetail, eDateTime, eOutcome, eoDetail, of_premis, fw_tab)

        #self.bcGenPremisEvent(root, eventIdType, eventIdVal,  "File System Analysis", eDateTime, eOutcome, eoDetail, of_premis, fw_tab)
        return root

    def bcGenPremisXmlBulkExtractor(self, beReportFile, premis_file, isFirstEvent=False):
        # Extract some values from the corresponding input XML file
        beReportXml_command_line = fiwalk.fiwalk_xml_command_line(beReportFile)

        image_name = self.extractImageName(beReportXml_command_line, "be")
        be_version = fiwalk.fiwalk_xml_version(beReportFile)

        # BE is the last event. So open the outfile to write
        if not os.path.exists(premis_file):
            of_premis = open(premis_file,"wb")
        else:
            of_premis = "null"

        print(">>> Generating bulk_extractor Premis Event")

        eventIdType = 0  # If this is 0, we will generate UUID

        #eventIdVal = beReportXml_command_line
        eventDetail = beReportXml_command_line

        eventType = "bulk_extractor"
        eDateTime = fiwalk.fiwalk_xml_start_time(beReportFile)

        # We don't check the flag for eOutcome as we don't run the 
        # bulk extractor on command line. We already have th feature files
        # from a previous run of the beViewer. We just use the information from
        # the report.xml file for generating premis events.
        eOutcome = "Completed" 

        # FIXME: Need more input on what to extract for Details
        eoDetail = "bulk_extractor version: "+be_version

        line1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        of_premis.write(bytes(line1, 'UTF-8'))

        self.bcGenPremisEvent(root, eventIdType, eventType, eventDetail, eDateTime, eOutcome, eoDetail, of_premis, True)
        
if __name__=="__main__":
    import sys, time, re

    parser = ArgumentParser(prog='bc_premis_genxml.py', description='Generate PREMIS XML file for BitCurator events')
    parser.add_argument('--dfxmlfile', action='store', help="DFXML file ")
    parser.add_argument('--bulk_extractor', action='store', help=" Bulk-extrator Report file ")
    parser.add_argument('--Allreports', action='store', help=' All Reports')
    parser.add_argument('--premis_file',action='store',help='Output Premis File; Concatinates if exists')

    args = parser.parse_args()
   
    print("D: dfxmlfile: ", args.dfxmlfile)
    print("D: output premis file", args.premis_file)

    premis = BcPremisFile()

    '''
    if (args.bulk_extractor):
        bcGenPremisXmlBulkExtractor(self, reportsFile, premis_file, outcome=True)
    '''
        
    premis.bcGenPremisXmlFiwalk(args.dfxmlfile, args.premis_file)

