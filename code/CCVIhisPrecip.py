#Brian Watson
#
#CCVIhisPrecip.py
#Warning:  This does not take into account 2 standard deviations as suggested in CCVI documentation
# Given the size of these ranges, this was not necessary.  Standard deviation should be implemented in further use of this code.

import arcpy, sys, os

arcpy.env.overwriteOutput = True
arcpy.env.workspace = "C:/GIS/!Final/data/output/CCVI_MultiExample/ranges"
arcpy.env.cellSize = "MINOF"
arcpy.CheckOutExtension("Spatial")

hismoisX = "C:/GIS/Automate/climate/histprecipmm"

arcpy.env.overwriteOutput = True

rasList = arcpy.ListRasters()
outPath = "C:/GIS/!Final/data/output/CCVI_MultiExample/CCVIhisPrecip"
if not os.path.exists(outPath):
    os.makedirs(outPath)
####################################################
for ras in rasList:
    outputFile = outPath + '/' +  ras
    outRas = arcpy.sa.Raster(ras) * arcpy.sa.Raster(hismoisX)
    outRas.save(outputFile)

    #get max and min value
    maxval = arcpy.GetRasterProperties_management(outputFile, "MAXIMUM")
    maxval = maxval.getOutput(0)
    minval = arcpy.GetRasterProperties_management(outputFile, "MINIMUM")
    minval = minval.getOutput(0)

    #subtract max min
    rasrange = float(maxval) - float(minval)
    print ras
    #print results and CCVI category
    if rasrange < 100:
        print "Greatly Increase"

    elif rasrange >= 100 and rasrange <= 254:
        print "Increase"

    elif rasrange >= 255 and rasrange <= 508:
        print "Somewhat Increase"

    elif rasrange >= 509 and rasrange <= 1016:
        print "Neutral"

    else:
        print "Somewhat Decrease"

    print rasrange
    print ""
