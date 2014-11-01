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

import arcpy, os
rangePath = 'C:/GIS/Automate'
arcpy.env.workspace = rangePath
arcpy.env.overwriteOutput = True

listFC = arcpy.ListFeatureClasses()
areaField = "Area_SqKM"

outpath = rangePath + '/dissolved'

if not os.path.exists(outpath):
    os.makedirs(outpath)
for FC in listFC:
    outfeature = outpath + '/' + FC
    arcpy.Dissolve_management(FC, outfeature, "","", True)
    arcpy.AddField_management(outfeature, areaField, "DOUBLE")
    exp = "float(!SHAPE.AREA@SQUAREKILOMETERS!)"
    arcpy.CalculateField_management(outfeature, areaField, exp, "PYTHON")
