#-------------------------------------------------------------------------------
# Name:        CCVIhisTemp.py
# Purpose:
#
# Author:      bwatson
#
# Created:     09/12/2013
# Copyright:   (c) bwatson 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, sys, os


arcpy.env.workspace = "C:/GIS/!Final/data/output/CCVI_MultiExample/ranges"
arcpy.env.cellSize = "MINOF"
arcpy.CheckOutExtension("Spatial")

histempX = "C:/GIS/Automate/climate/histtempvarc"

arcpy.env.overwriteOutput = True

rasList = arcpy.ListRasters()
outPath = "C:/GIS/!Final/data/output/CCVI_MultiExample/CCVIhisTemp"
if not os.path.exists(outPath):
    os.makedirs(outPath)

#loop through and multiply
for raster in rasList:
    outputFile =  outPath + '/' + raster
    outHisTemp = arcpy.sa.Raster(raster) * arcpy.sa.Raster(histempX)
    arcpy.CalculateStatistics_management(outHisTemp)
    #reclassify
    outRecRas = arcpy.sa.Reclassify(outHisTemp, "Value",
                        arcpy.sa.RemapRange([[0, 20.8, 5], [20.8, 26.3, 4], [26.3, 31.8, 3], [31.8, 43.0, 2], [43.0, 100, 1]]))

    outRecRas.save(outputFile)

    #list fields and add percentage field if does not exist
    listF = arcpy.ListFields(outputFile)
    x = []
    for field in listF:
        x.append(field.name)
    if not "PERCENTAGE" in x:
        arcpy.AddField_management(outputFile, "PERCENTAGE", "DOUBLE")

     #check for path for stats tables, if doesn't exist create
    statsPath = outPath + '/STATStables'
    if not os.path.exists(statsPath):
        os.makedirs(statsPath)

    outStats = statsPath + '/' + raster

    arcpy.Statistics_analysis(outputFile, outStats, [["COUNT", "SUM"]])
    with arcpy.da.SearchCursor(outStats, ["SUM_COUNT"]) as cursor:
        row = cursor.next()
        sumCount = row[0]
    sumCountX = str(sumCount)
    expression = "float(!COUNT!) / " + sumCountX
    arcpy.CalculateField_management(outputFile, "PERCENTAGE", expression, "PYTHON_9.3")
    arcpy.BuildPyramidsandStatistics_management(outputFile)