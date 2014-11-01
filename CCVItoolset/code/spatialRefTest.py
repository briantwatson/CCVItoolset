#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      bwatson
#
# Created:     11/12/2013
# Copyright:   (c) bwatson 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
rangePath = 'C:/GIS/!Final/data/output/CCVI_MultiExample/ranges'
arcpy.env.workspasce = rangePath

listFC = arcpy.ListFeatureClasses()
newPath = rangePath + '/reproject'

for FC in listFC:
    outPath = newPath + '/' + FC
    arcpy.Project_management(FC, outPath, 'project.prj')
