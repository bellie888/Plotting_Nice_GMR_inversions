# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 11:24:00 2017

@author: Joseph Bell

This script is designed to read a series of excel files and plot reasonably modern
charts from the data. It is specifically for Ground Magnetic Resonance inversion data
so that the data can be visualised.

The script makes use of Pandas and ggplot in addition to matplotlib

Features:
    + the y axis has zero at the top because we are looking at depths below ground level
    + the depth of investigation horizontal line is determined by the data
    + pandas is used to filter the data were needed.
    + axis are named
    + all graphs are on the same x scale (40% max water content) to be comparable
    + dpi of the output png files is ajustable

Further improvement could be a smoothing function to take the jaggies out of the lines.

Dependancies:
    pandas 0.2 for read excel
"""

import matplotlib.pyplot as plt
import matplotlib
#print matplotlib.__version__
import os


import pandas as pd

# find the version of Pandas you have
print "Pandas Version " + str(pd.__version__)


# point to the folder with all the excel GMR inversions
# full path name removed for security
workFolder = r'Your path\GMR_coords_inversion_data/'

unfound = list()

#site names convert.
 
def findSiteNumber(name):
    global unfound
    # This function converts the excel file name to a site number on the map for improved visualisation
    sites = [['104201_trans_st10', ' 0'],['104201_trans_st11', ' 1'],['104201_trans_st2', ' 2'],
            ['104201_trans_st4', ' 3'],['104201_trans_st6', ' 4'],['104201_trans_st7', ' 5'],
            ['104201_trans_st9', ' 6'],['1pm', ' 7'],['2pm', ' 8'],['4m', ' 9'],['6m', ' 10'],['7m', ' 11'],
            ['central_spat_cov_st1', ' 12'],['central_spat_cov_st2', ' 13'],['Coal_Bore_Reg_st1', ' 14'],['DAFWA_bore', ' 15'],
            ['springs_delta_st2', ' 16'],['east_spat_cov_st1', ' 17'],['horst_trans_st1', ' 18'],
            ['horst_trans_st2', ' 19'],['horst_trans_st3', ' 20'],['horst_trans_st4', ' 21'],['horst_trans_st5', ' 22'],
            ['horst_trans_st6', ' 23'],['MillProf', ' 24'],['SaltFlats_St1', ' 25'],['springs_delta_st1', ' 26'],
            ['springs_delta_st3', ' 27'],['strat_trans_st2', ' 28'],['strat_trans_st3', ' 29'],['sw_spat_cov_st1', ' 30'],
            ['swi_st1', ' 31'],['swi_st2', ' 32'],['swi_st5', ' 33'],['swi_st6', ' 34'],['yow_bore_', ' 35'],
            ['105501_trans_st3', ' 36']]
    
    found = False
    for item in sites:
        # print item[0], item[1]
        if item[0] in name:
            print "found " + item[1]
            thisName = "Site " + item[1]
            found = True
    if not found:
        unfound.append(name)
        return name
    else:
        return thisName


   
# list of xlsx files
fList = os.listdir(workFolder)

# define a list to hold the file names
theseFiles = list()


# choose only the exel files - others are ignored
for item in fList:
    if item.endswith('.xlsx'):
        theseFiles.append(item)
        # print item
        
        
for item in theseFiles:
    
    # full path to the file
    thisFile = workFolder + item


    #thisData = pd.read_csv(thisFile)  - csv alternative
    thisData = pd.read_excel(thisFile)
   
    
    # print item
    # work out DOI using pandas functions
    isDOI = thisData[thisData['Depth of Investigation'] == '<DOI']
    maxDepth = isDOI['lower depth m'].max()
    
#    print 'type m' + str(type(maxDepth))
#    
#    print isDOI.head()
#    
#    print 'max Depth ' + str(maxDepth) 
#    print
#    
#    print 'processing ' + item
#    print
    
    # Create a figure of size 8x6 inches, 300 dots per inch
    plt.figure(figsize=(6, 8), dpi=300)
    
    # use the ggplot style
    plt.style.use('ggplot')
    
    # invert the y axix so that depth in a positive number
    plt.gca().invert_yaxis()
    
    # set the range on the x axis so all the plots are the same scale
    plt.xlim([-2,40])
    

    # plot DOI horzontal line
    plt.hlines(maxDepth, 0, 40, color = 'brown', 
               linestyles = 'dotted')
    
    # define plot data using pandas series names
    y = thisData['Upper depth m']
    Total = thisData['Total H2O'] * 100
    Mobile = thisData['Mobile H2O'] * 100
    Bound = thisData['Bound H2O'] * 100
    
    
    # convert filename to SiteName if possible
    # if unfound returns orininal filename
    mytitle = findSiteNumber(item)
    
    # plot the title Site Number
    plt.title(mytitle, loc ='left')
    # plot the righthand small filename
    plt.title(item, loc ='right', fontsize = 7)
    
#    # remove extesion of file name
#    thisFileName = item.replace('.xlsx', '')
#    
#    # add a bit of text with the file name
#    plt.text(20,18, thisFileName, fontsize = 8)

    # plot comment on DOI line
    plt.text(19, (maxDepth-1), 'Maximum tenable depth of investigation',  fontsize = 8)
    
 
    # plot lines
    plt.plot(Total, y, label = 'Total H2O')
    plt.plot(Mobile, y, label = 'Mobile H2O')
    plt.plot(Bound, y, label = 'Bound H2O')
    
    # make legend
    plt.legend()
    
    # define axis names
    plt.ylabel('Depth (upper) m')
    plt.xlabel('Water content %')
    
    
    # name the outfie as png
    
    outFile = workFolder + (item.replace('.xlsx', ''))
    
    # save the png
    plt.savefig(outFile)
    
    # optional - shows plot in console - sometimes it dose anyway
    #plt.show()
    

#
# optional part of finding plotnames tha tneed to be converted
print "Unfound plot names"
for item in unfound:
    print item


print "finished"
