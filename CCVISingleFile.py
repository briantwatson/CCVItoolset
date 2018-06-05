#Brian Watson, btwatso2
#
#CCVISingleFile.py

import sys, os
toolspath = os.path.dirname(sys.argv[0]) + '/code'
sys.path.append(toolspath)

import CCVITools, arcpy

arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.SetProgressor('default')
#take input arguments
### input file, input file field with species identifier, input predicted
### moisture raster path, input predicted temp raster path, project name
###

inFile = arcpy.GetParameterAsText(0)
inField = arcpy.GetParameterAsText(1)
inMois = arcpy.GetParameterAsText(2)
inTemp = arcpy.GetParameterAsText(3)
project = arcpy.GetParameterAsText(4)

###Hardcoded for testing###
#inFile = "C:/GIS/Counties.gdb/MergedCounties"
#inField = "Species"
#inMois = "C:\\GIS\\Automate\\climate\\moispred2050"
#inTemp = "C:\\GIS\\Automate\\climate\\temppred2050"
#project = "CCVITest"

scriptPath = os.path.dirname(sys.argv[0])

projNoSp = project.replace(" ", "_")

folderLoc = scriptPath + '/data/output/' + projNoSp
rangeLoc = folderLoc + '/ranges'
if not os.path.exists(folderLoc):
    os.makedirs(folderLoc)
if not os.path.exists(rangeLoc):
    os.makedirs(rangeLoc)

CCVITools.AddMsg("Converting unique features to seperate files")
#  One file, run proc to generate new species files,
CCVITools.oneFileSpecies(inFile, inField, rangeLoc)

###Hardcoded for testing###
###rangePath = 'C:/CCVIGIS/CCVITest/ranges'

# list polygons (from here down can be copied for script when individual
# species POLYGON files already exist
arcpy.env.workspace = rangeLoc
arcpy.env.overwriteOutput = True

listFC = arcpy.ListFeatureClasses()

#add field with value of '1' to each polygon, and convert to raster
for FC in listFC:
    CCVITools.fieldAdder(FC)
    outRasName = CCVITools.shortenFileName(FC)
    outMsg = "Converting {0} to raster".format(FC)
    CCVITools.AddMsg(outMsg)
    CCVITools.polygonToRaster(rangeLoc, FC, outRasName)

#list rasters (from here down can be copied for script when individual
# species RASTER files already exist
listRas = arcpy.ListRasters()

#run tools
for ras in listRas:
    outMsg = "Creating CCVI Shapefiles for {0}".format(ras)
    CCVITools.AddMsg(outMsg)
    CCVITools.CCVIpredTemp(ras, inTemp, folderLoc)
    CCVITools.CCVIpredMois(ras, inMois, folderLoc)


#add to Map
mxdPath = scriptPath + '/CCVI_Template.mxd'
mxd = arcpy.mapping.MapDocument("CURRENT")
dfs = arcpy.mapping.ListDataFrames(mxd)
df = dfs[0]
targetGroupLayer = arcpy.mapping.ListLayers(mxd, "*", df)[0]
targetGroupLayer2 = arcpy.mapping.ListLayers(mxd, "*", df)[1]

#add predicted moisture results to map
outMsg = "Adding predicted moisture results to map"
CCVITools.AddMsg(outMsg)
predMoisResults = folderLoc + '/CCVIpredMois'
arcpy.env.workspace = predMoisResults
listRas = arcpy.ListRasters()
for ras in listRas:
    filePath = predMoisResults + '/' + ras
    addLayer = arcpy.mapping.Layer(filePath)
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, addLayer)


#add predicted temp results to map
outMsg = "Adding predicted temperature results to map"
CCVITools.AddMsg(outMsg)
predTempResults = folderLoc + '/CCVIpredTemp'
arcpy.env.workspace = predTempResults
listRas = arcpy.ListRasters()

CCVITools.AddMsg(targetGroupLayer)
for ras in listRas:
    filePath = predTempResults + '/' + ras
    addLayer = arcpy.mapping.Layer(filePath)
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer2, addLayer)

del mxd
