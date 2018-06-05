#Brian Watson, btwatso2
#
#CCVITools.py
import arcpy, sys, os
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
cellSizeLoc = sys.argv[0] + '/cellsize'
arcpy.env.cellSize = cellSizeLoc

def AddMsg(message):
    arcpy.AddMessage(message)

def shortenFileName(inName):
    """take input species binomial separated by space or underscore \
    and returns 13 char name for raster file.  e.g. 'Conradina verticillata'\
    becomes  'C_verticallat'"""
    #try spliting by space
    inName = os.path.splitext(inName)[0]
    splitName = inName.split(" ")

    #check if name didn't split and try splitting by underscore
    if len(splitName) == 1:
        splitName = inName.split("_")

    if len(splitName) == 2:
        outName = (splitName[0][0] + '_' + splitName[1])[0:13]
    else:
        outName = inName[0:13]
    return outName


def polygonToRaster(rangePath, inFile, outName):
    outFile =  rangePath + '/' + outName
    if not os.path.exists(outFile):
        arcpy.PolygonToRaster_conversion(inFile, "CCVIField1", outFile, "",\
         "CCVIField1")

def fieldAdder(file):
    listF = arcpy.ListFields(file)
    listFieldNames = [field.name for field in listF]
    if not "CCVIField1" in listFieldNames:
        arcpy.AddField_management(file, "CCVIField1", "SHORT")
        arcpy.CalculateField_management(file, "CCVIField1",1, "PYTHON")

#def createProjGDB(projName):
    #"""Creates GDB for project under C:/CCVIGIS, returns path of GDB"""
    #if not os.path.exists('C:/CCVIGIS'):
    #    os.makedirs('C:/CCVIGIS')
    #arcpy.CreateFileGDB_management('C:/CCVIGIS', projName)
    #fullPath = 'C:/CCVIGIS/' + projName
    #return fullPath


def oneFileSpecies(fileN, fieldN, rangeLoc):
    """Get species list for given File"""
    valueList = []
    with arcpy.da.SearchCursor(fileN, fieldN) as cursor:
        for row in cursor:
            valueList.append(row[0])

    S = set(valueList)
    speciesList = []

    for i in S:
        speciesList.append(i)

    speciesList.sort()
    for x in speciesList:
        xformat = x.replace(" ", "_")
        xformat = x.replace(".", "")
        outputFile = rangeLoc + '/' + xformat + ".shp"
        whereClause = "\"" + fieldN + "\" = " +"'"+ x + "'"
        arcpy.Select_analysis(fileN, outputFile, whereClause)



def CCVIpredTemp(raster, predTempX, folderLoc):
    #pass in file and location of predicted temp file
    """creates new file with predicted temp categories for CCVI"""

    #multiply rangefile by predicted temp file
    tempRas = arcpy.sa.Raster(raster) * arcpy.sa.Raster(predTempX)
    arcpy.CalculateStatistics_management(tempRas)
    outRecRas = arcpy.sa.Reclassify(tempRas, "Value", arcpy.sa.RemapRange([[0, 3.9, 1], [3.9, 4.4, 2], [4.4, 5.0, 3], [5.0, 5.5, 4], [5.5, 100, 5]]))

    predTempPath = folderLoc + '/CCVIpredTemp'
    if not os.path.exists(predTempPath):
        os.makedirs(predTempPath)
    outFile =  predTempPath + '/' + raster
    outRecRas.save(outFile)

    #calculate percentage of field of total and add field to raster
    listF = arcpy.ListFields(outFile)
    x = []
    for field in listF:
        x.append(field.name)
    if not "PERCENTAGE" in x:
        arcpy.AddField_management(outFile, "PERCENTAGE", "DOUBLE")


    #check for path for stats tables, if doesn't exist create
    statsPath = predTempPath + '/STATStables'
    if not os.path.exists(statsPath):
        os.makedirs(statsPath)

    #create stats table
    outStats = statsPath + '/' + raster
    arcpy.Statistics_analysis(outFile, outStats, [["COUNT", "SUM"]])

    #find sum of total cells
    with arcpy.da.SearchCursor(outStats, ["SUM_COUNT"]) as cursor:
        row = cursor.next()
        sumCount = row[0]
    sumCountX = str(sumCount)
    expression = "float(!COUNT!) / "+ sumCountX
    arcpy.CalculateField_management(outFile, "PERCENTAGE", expression, "PYTHON_9.3")
    arcpy.BuildPyramidsandStatistics_management(outFile)


def CCVIpredMois(raster, predMoisX, folderLoc):
    """creates new file with predicted moisture categories for CCVI"""

    #multiply rangefile by predicted temp file
    moistRas = arcpy.sa.Raster(raster) * arcpy.sa.Raster(predMoisX)
    arcpy.CalculateStatistics_management(moistRas)
    outRecRas = arcpy.sa.Reclassify(moistRas, "Value",
                        arcpy.sa.RemapRange([[-999, -0.119, 6], \
                        [-0.119, -0.096, 5], [-0.096, -0.073, 4], \
                        [-0.073, -0.050, 3], [-0.050, -0.028, 2], \
                        [-0.028, 998, 1]]))

    predMoisPath = folderLoc + '/CCVIpredMois'
    if not os.path.exists(predMoisPath):
        os.makedirs(predMoisPath)
    outFile =  predMoisPath + '/' + raster
    outRecRas.save(outFile)

    #calculate percentage of field of total and add field to raster
    listF = arcpy.ListFields(outFile)
    x = []
    for field in listF:
        x.append(field.name)
    if not "PERCENTAGE" in x:
        arcpy.AddField_management(outFile, "PERCENTAGE", "DOUBLE")


    #check for path for stats tables, if doesn't exist create
    statsPath = predMoisPath + '/STATStables'
    if not os.path.exists(statsPath):
        os.makedirs(statsPath)
    outStats = statsPath + '/' + raster
    arcpy.Statistics_analysis(outFile, outStats, [["COUNT", "SUM"]])
    with arcpy.da.SearchCursor(outStats, ["SUM_COUNT"]) as cursor:
        row = cursor.next()
        sumCount = row[0]
    sumCountX = str(sumCount)
    expression = "float(!COUNT!) / " + sumCountX
    arcpy.CalculateField_management(outFile, "PERCENTAGE", expression, "PYTHON_9.3")
    arcpy.BuildPyramidsandStatistics_management(outFile)
