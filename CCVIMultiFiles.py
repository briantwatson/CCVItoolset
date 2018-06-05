#Brian Watson, btwatso2
#
#CCVIMultiFiles.py

import sys, os

scriptPath = os.path.dirname(sys.argv[0])
toolspath = scriptPath + '/code'
sys.path.append(toolspath)

import CCVITools, arcpy

#arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.SetProgressor('default')
#take input arguments
### input file, input file field with species identifier, input predicted
### moisture raster path, input predicted temp raster path, project name
###

inFolder = arcpy.GetParameterAsText(0)
inMois = arcpy.GetParameterAsText(1)
inTemp = arcpy.GetParameterAsText(2)
project = arcpy.GetParameterAsText(3)

projNoSp = project.replace(" ", "_")

#create necessary folders
folderLoc = scriptPath + '/data/output/' + projNoSp
rangeLoc = folderLoc + '/ranges'
if not os.path.exists(folderLoc):
    os.makedirs(folderLoc)
if not os.path.exists(rangeLoc):
    os.makedirs(rangeLoc)

#if feature classes, copy features in folder to working folder under C:/CCVIGIS/$project/ranges, where $project is the name of the project passed in from the script tool
arcpy.env.workspace = inFolder
listFC = arcpy.ListFeatureClasses()
CCVITools.AddMsg('\n')
CCVITools.AddMsg("Copying files to working folder")
CCVITools.AddMsg('\n')
if len(listFC) >= 1:
    for FC in listFC:
        outFeature = rangeLoc + '/' + FC
        arcpy.CopyFeatures_management(FC, outFeature)

#or if rasters present, copy rasters
listRas = arcpy.ListRasters()
if len(listRas) >= 1:
    for ras in listRas:
        outRas = rangeLoc + '/' + ras
        arcpy.CopyRaster_management(ras, outRas)

#set workspace to working folder under C:/CCVIGIS
arcpy.env.workspace = rangeLoc
listWFC = arcpy.ListFeatureClasses()

#add number field for conversion and convert to raster
for WFC in listWFC:
    CCVITools.fieldAdder(WFC)
    outRasName = CCVITools.shortenFileName(WFC)
    outMsg = "Converting {0} to raster".format(WFC)
    CCVITools.AddMsg(outMsg)
    CCVITools.polygonToRaster(rangeLoc, WFC, outRasName)

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