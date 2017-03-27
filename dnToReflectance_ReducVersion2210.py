#-------------------------------------------------------------------------------
# Name:        dnToReflectance.py
# Purpose:     Create a dict from metadata file usable to assign variables and
#              Perform DN to Reflectance rescaling.
#
# Author:      Simon Bardsley
#
# Created:     19/06/2013
# Modified:    27/03/2017
# Licence:Creative Commons BY 4.0
#-------------------------------------------------------------------------------
print "Importing modules..."
import os, sys, io, arcpy, math
from arcpy.sa import *
from arcpy import env
env.overwriteOutput = True

print "Checking out Extention_sa"
#Check out any necessary licences
arcpy.CheckOutExtension("Spatial")

path = "C:/gisdata/india/imagery/"
parentdir = "off"

dirname = []
pathfolders = []
for fname in os.listdir(path + parentdir):
  if not os.path.isfile(os.path.join(path + parentdir, fname)):
    dirname.append(fname)

print "Directory names " + str(dirname)

#Loop through image directories and list the tif raster files within each and
#process to reflectance values
for dir in dirname:
    #Set workspace to current working directory
    env.workspace = path + parentdir + "/" + dir
    print "Workspace is " + str(env.workspace)

    #Set the directory to each imagery directory looped through one at a time
    rasterfiles = os.chdir(path + parentdir + "/" + dir)
    #Get the current working directory to see that directory has changed
    curdir = os.getcwd()
    print "Current working directory is " + curdir
    #Set the env workspace to the current working directory
    env.workspace = curdir
    #Enlist and show all tif raster files within the current working directory
    rasterlist = arcpy.ListRasters("*", "TIF")
    for rasters in rasterlist:
        print rasters

    print ""
    #Check out any necessary licences
    arcpy.CheckOutExtension("Spatial")
    print "Spatial Analyst extension checked out!"

    print ""
    #Set workspace to C drive
    env.workspace = path + parentdir + "/" + dir
    print "Workspace is set to c:drive directory: "

    print "*************************************************************************"
    print "Opening metadatafile for dict creation"
    print ""
    #Open Metadata file for reading
    f = io.open(path + parentdir + "/" + dir + "/" + dir + "_MTL.txt","r")

    print "Creating dict object..."
    def build_data(f): #build dictionary

        output = {} #Dict
        for line in f.readlines(): #Iterates through every line in the string
            if "=" in line: #make sure line has data as wanted
                l = line.split("=") #Seperate by "=" and put into a list
                output[l[0].strip()] = l[1].strip() #First word is key, second word is value

        return output #Returns a dictionary with the key, value pairs.

    data = build_data(f)

    f.close()
    print "Closing metadata file!"
    print ""
    print "*************************************************************************"
    print "*** Extracting metadata ***"
    print ""

    dataType = str(data["DATA_TYPE"])
    print "Data Type = " + dataType

    #Test whether dataType is equal to L1T (the minimum processing level to process)
    if dataType == '"L1T"':
        print "Data Type is L1T"
    else:
        print "Data Type is not L1T"
        exit() #Exit should be replaced by skipping the image that does not have sufficent processing level

    #Extract landsat scene information fron dictionary file
    landsatSceneID = str(data["LANDSAT_SCENE_ID"])
    print "Scene ID = " + landsatSceneID

    print "*************************************************************************"
    print "*** Extracting Julian Day infomation ***"
    print ""

    #Extract Julian day from landsat scene id
    julianDay = int(landsatSceneID[14:17])
    print "Julian Day = " + str(julianDay)

    print "*************************************************************************"
    print "*** Printing Radiance variables: ***"
    print ""

    # Convert dict entry to variable classes and print ouput to screen
    LMin_B1 = float(data["RADIANCE_MINIMUM_BAND_1"])
    print "LMIN_B1 = " + str(LMin_B1)
    LMax_B1 = float(data["RADIANCE_MAXIMUM_BAND_1"])
    print "LMAX_B1 = " + str(LMax_B1)
    LMin_B2 = float(data["RADIANCE_MINIMUM_BAND_2"])
    print "LMIN_B2 = " + str(LMin_B2)
    LMax_B2 = float(data["RADIANCE_MAXIMUM_BAND_2"])
    print "LMAX_B2 = " + str(LMax_B2)
    LMin_B3 = float(data["RADIANCE_MINIMUM_BAND_3"])
    print "LMIN_B3 = " + str(LMin_B3)
    LMax_B3 = float(data["RADIANCE_MAXIMUM_BAND_3"])
    print "LMAX_B3 = " + str(LMax_B3)
    LMin_B4 = float(data["RADIANCE_MINIMUM_BAND_4"])
    print "LMIN_B4 = " + str(LMin_B4)
    LMax_B4 = float(data["RADIANCE_MAXIMUM_BAND_4"])
    print "LMAX_B4 = " + str(LMax_B4)

    print "*************************************************************************"
    print "*** Printing Quantize CAL variables: ***"
    print ""

    # Convert QCAL values from dict to variable class values
    QCALMax_B1 = float(data["QUANTIZE_CAL_MAX_BAND_1"])
    print "QCALMax_B1 = " + str(QCALMax_B1)
    QCALMin_B1 = float(data["QUANTIZE_CAL_MIN_BAND_1"])
    print "QCALMin_B1 = " + str(QCALMin_B1)
    QCALMax_B2 = float(data["QUANTIZE_CAL_MAX_BAND_2"])
    print "QCALMax_B2 = " + str(QCALMax_B2)
    QCALMin_B2 = float(data["QUANTIZE_CAL_MIN_BAND_2"])
    print "QCALMin_B2 = " + str(QCALMin_B2)
    QCALMax_B3 = float(data["QUANTIZE_CAL_MAX_BAND_3"])
    print "QCALMax_B3 = " + str(QCALMax_B3)
    QCALMin_B3 = float(data["QUANTIZE_CAL_MIN_BAND_3"])
    print "QCALMin_B3 = " + str(QCALMin_B3)
    QCALMax_B4 = float(data["QUANTIZE_CAL_MAX_BAND_4"])
    print "QCALMax_B4 = " + str(QCALMax_B4)
    QCALMin_B4 = float(data["QUANTIZE_CAL_MIN_BAND_4"])
    print "QCALMin_B4 = " + str(QCALMin_B4)

    print ""
    print "Creating local variables for input bands"

    outSetNull1 = path + parentdir + "/" + dir + "/" + "outSetNull1"
    outSetNull2 = path + parentdir + "/" + dir + "/" + "outSetNull2"
    outSetNull3 = path + parentdir + "/" + dir + "/" + "outSetNull3"
    outSetNull4 = path + parentdir + "/" + dir + "/" + "outSetNull4"

    #Local variable - input bands (uncomment these to go back to having zeros in boarder and gaps)
##    b1 = Raster(path + parentdir + "/"  + dir + "/" + dir + "_B1.TIF")
##    b2 = Raster(path + parentdir + "/"  + dir + "/" + dir + "_B2.TIF")
##    b3 = Raster(path + parentdir + "/"  + dir + "/" + dir + "_B3.TIF")
##    b4 = Raster(path + parentdir + "/"  + dir + "/" + dir + "_B4.TIF")

    print "Creating output band variables"
    #Output variables
    L_B1 = path + parentdir + "/" + dir + "/" + "L_B1"
    L_B2 = path + parentdir + "/" + dir + "/" + "L_B2"
    L_B3 = path + parentdir + "/" + dir + "/" + "L_B3"
    L_B4 = path + parentdir + "/" + dir + "/" + "L_B4"
    L_bcomp = path + parentdir + "/" + dir + "/" + "L_bcomp"

    print "Converting zero values to null"
    #Change zero values to null values in scene boarder and in gaps (comment these out to stop converting zeros to null values)
    if arcpy.Exists(outSetNull1):
        arcpy.Delete_management(outSetNull1)
    outSetNull1 = SetNull(path + parentdir + "/"  + dir + "/" + dir + "_B1.TIF",path + parentdir + "/"  + dir + "/" + dir + "_B1.TIF", "VALUE = 0")
    outSetNull1.save(path + parentdir + "/"  + dir + "/" + "SetNull1.TIF")

    if arcpy.Exists(outSetNull2):
        arcpy.Delete_management(outSetNull2)
    outSetNull2 = SetNull(path + parentdir + "/"  + dir + "/" + dir + "_B2.TIF",path + parentdir + "/"  + dir + "/" + dir + "_B2.TIF", "VALUE = 0")
    outSetNull2.save(path + parentdir + "/"  + dir + "/" + "SetNull2.TIF")

    if arcpy.Exists(outSetNull3):
        arcpy.Delete_management(outSetNull3)
    outSetNull3 = SetNull(path + parentdir + "/"  + dir + "/" + dir + "_B3.TIF",path + parentdir + "/"  + dir + "/" + dir + "_B3.TIF", "VALUE = 0")
    outSetNull3.save(path + parentdir + "/"  + dir + "/" + "SetNull3.TIF")

    if arcpy.Exists(outSetNull4):
        arcpy.Delete_management(outSetNull4)
    outSetNull4 = SetNull(path + parentdir + "/"  + dir + "/" + dir + "_B4.TIF",path + parentdir + "/"  + dir + "/" + dir + "_B4.TIF", "VALUE = 0")
    outSetNull4.save(path + parentdir + "/"  + dir + "/" + "SetNull4.TIF")

    # Define outSetNulls as variable (comment out this if you want to go back to having zero values in boarder and gaps)
    b1 = Raster(path + parentdir + "/"  + dir + "/" + "SetNull1.TIF")
    b2 = Raster(path + parentdir + "/"  + dir + "/" + "SetNull2.TIF")
    b3 = Raster(path + parentdir + "/"  + dir + "/" + "SetNull3.TIF")
    b4 = Raster(path + parentdir + "/"  + dir + "/" + "SetNull4.TIF")

    print "*************************************************************************"
    # Digital Number conversion to Top of Atmosphere Radiance Values
    print "*** Performing band calculations: ***"
    print"*** Spectral Radiance Scaling Method ***"
    print""

    print "starting L_B1 (1 of 4)"
    if arcpy.Exists(L_B1):
        arcpy.Delete_management(L_B1)
    L_B1 = (float(LMax_B1)-float(LMin_B1))/(float(QCALMax_B1)-float(QCALMin_B1))*(b1-float(QCALMin_B1))+float(LMin_B1)
    L_B1.save(path + parentdir + "/" + dir + "/" + "L_B1.TIF")
    print "L_B1 has been created"

    print "Starting L_B2 (2 of 4)"
    if arcpy.Exists(L_B2):
        arcpy.Delete_management(L_B2)
    L_B2 = (float(LMax_B2)-float(LMin_B2))/(float(QCALMax_B2)-float(QCALMin_B2))*(b2-float(QCALMin_B2))+float(LMin_B2)
    L_B2.save(path + parentdir + "/" + dir + "/" + "L_B2.TIF")
    print "L_B2 has been created"

    print "Starting L_B3 (3 of 4)"
    if arcpy.Exists(L_B3):
        arcpy.Delete_management(L_B3)
    L_B3 = (float(LMax_B3)-float(LMin_B3))/(float(QCALMax_B3)-float(QCALMin_B3))*(b3-float(QCALMin_B3))+float(LMin_B3)
    L_B3.save(path + parentdir + "/" + dir + "/" + "L_B3.TIF")
    print "L_B3 has been created"

    print "Starting L_B4 (4 of 4)"
    if arcpy.Exists(L_B4):
        arcpy.Delete_management(L_B4)
    L_B4 = (float(LMax_B4)-float(LMin_B4))/(float(QCALMax_B4)-float(QCALMin_B4))*(b4-float(QCALMin_B4))+float(LMin_B4)
    L_B4.save(path + parentdir + "/" + dir + "/" + "L_B4.TIF")
    print "L_B4 has been created"


    print "*************************************************************************"
    print"***Performing Radiance to ToA Reflectance***"
    print""

    #Create found_distances dictonary = julian day / earth-sun distance values
    day_distances =    [(1, 0.9832),
                        (15, 0.9836),
                        (32, 0.9853),
                        (46, 0.9878),
                        (60, 0.9909),
                        (74, 0.9945),
                        (91, 0.9993),
                        (106, 1.0033),
                        (121, 1.0076),
                        (135, 1.0109),
                        (152, 1.0140),
                        (166, 1.0158),
                        (182, 1.0167),
                        (196, 1.0165),
                        (213, 1.0149),
                        (227, 1.0128),
                        (242, 1.0092),
                        (258, 1.0057),
                        (274, 1.0011),
                        (288, 0.9972),
                        (305, 0.9925),
                        (319, 0.9892),
                        (335, 0.9860),
                        (349, 0.9843),
                        (365, 0.9833),
                        ]

    found_distance = None

    #Use binary search algorithm to extract distance value from day_distances dictonary
    for day, distance in reversed(sorted(day_distances)):
        if day <= julianDay:
            found_distance = distance
            break

    print "Earth-Sun Distance = " + str(found_distance)

    print""
    print"Extracting solar Zenith Angle"
    print""

    zenith = float(data["SUN_ELEVATION"])

    print "Zenith = " + str(zenith)
    thetaSZrad = (zenith/180)*math.pi
    print""
    print "ThetaSZrad = " + str(thetaSZrad)
    print""

    #Local variable - input bands
    toa_b1 = (path + parentdir + "//"  + dir + "//" + "toa_b1.TIF")
    toa_b2 = (path + parentdir + "//"  + dir + "//" + "toa_b2.TIF")
    toa_b3 = (path + parentdir + "//"  + dir + "//" + "toa_b3.TIF")
    toa_b4 = (path + parentdir + "//"  + dir + "//" + "toa_b4.TIF")

    print "Starting toa_b1 (1 of 4)"
    if arcpy.Exists(toa_b1):
        arcpy.Delete_management(toa_b1)
    toa_b1 = (math.pi * L_B1 * found_distance) / (1969.000 * math.cos(thetaSZrad))
    toa_b1.save(path + parentdir + "/" + dir + "/" + "toa_b1.TIF")
    print "toa_b1 has been created"

    print "Starting toa_b2 (2 of 4)"
    if arcpy.Exists(toa_b2):
        arcpy.Delete_management(toa_b2)
    toa_b2 = (math.pi * L_B2 * found_distance) / (1840.000 * math.cos(thetaSZrad))
    toa_b2.save(path + parentdir + "/" + dir + "/" + "toa_b2.TIF")
    print "toa_b2 has been created"

    print "Starting toa_b3 (3 of 4)"
    if arcpy.Exists(toa_b3):
        arcpy.Delete_management(toa_b3)
    toa_b3 = (math.pi * L_B3 * found_distance) / (1551.000 * math.cos(thetaSZrad))
    toa_b3.save(path + parentdir + "/" + dir + "/" + "toa_b3.TIF")
    print "toa_b3 has been created"

    print "Starting toa_b4 (4 of 4)"
    if arcpy.Exists(toa_b4):
        arcpy.Delete_management(toa_b4)
    toa_b4 = (math.pi * L_B4 * found_distance) / (1044.000 * math.cos(thetaSZrad))
    toa_b4.save(path + parentdir + "/" + dir + "/" + "toa_b4.TIF")
    print "toa_b4 has been created"

    print "*************************************************************************"
    print "*** Performing Dark Pixel Subtraction method ***"
    print ""
    print "Creating local variables for input bands to Dark Pixel Subtraction"
    toa_b1dp = Raster(path + parentdir + "/" + dir + "/" + "toa_b1.TIF")
    toa_b2dp = Raster(path + parentdir + "/" + dir + "/" + "toa_b2.TIF")
    toa_b3dp = Raster(path + parentdir + "/" + dir + "/" + "toa_b3.TIF")
    toa_b4dp = Raster(path + parentdir + "/" + dir + "/" + "toa_b4.TIF")

    bands = ("toa_b1.TIF", "toa_b2.TIF", "toa_b3.TIF", "toa_b4.TIF")

    for band in bands:
        # Sampling current band's pixel values for the x,y points from Delhi_dp.shp
        arcpy.sa.Sample( band, "C:/gisdata/india/shapes/Delhi_dp.shp","sample1.dbf","NEAREST")
        print "Sampled raster values using selected points"

        # Selecting all rows from the sample table where the point location's pixel values for each band are above zero
        valueField = band[:-4]
        queryString = '"{0}" > 0' .format(valueField)
        rowcount = 0
        with arcpy.da.SearchCursor("sample1.dbf", (valueField), queryString) as cursor:
            for row in cursor: # This loop checks all rows per band and retains the band's lowest value for use in the dp subtraction outside the loop.
                rowcount += 1
                if rowcount == 1:
                    if valueField == "toa_b1":
                        dpb1value = row[0]
                    elif valueField == "toa_b2":
                        dpb2value = row[0]
                    elif valueField == "toa_b3":
                        dpb3value = row[0]
                    elif valueField == "toa_b4":
                        dpb4value = row[0]

                if valueField == "toa_b1":
                    if row[0] < dpb1value:
                        dpb1value = row[0]
                elif valueField == "toa_b2":
                    if row[0] < dpb2value:
                        dpb2value = row[0]
                elif valueField == "toa_b3":
                    if row[0] < dpb3value:
                        dpb3value = row[0]
                elif valueField == "toa_b4":
                    if row[0] < dpb4value:
                        dpb4value = row[0]

    print "lowest values: 1=" + str(dpb1value) + ", 2=" + str(dpb2value) + ", 3=" + str(dpb3value) + ", 4=" + str(dpb4value)
    toa_b1dp = toa_b1dp - dpb1value
    toa_b2dp = toa_b2dp - dpb2value
    toa_b3dp = toa_b3dp - dpb3value
    toa_b4dp = toa_b4dp - dpb4value
    print "Subtracted lowest dark pixel value from each band's dpRaster"

    print ""
    toa_b1dp.save(path + parentdir + "/" + dir + "/" + "toa_b1dp.TIF")
    toa_b2dp.save(path + parentdir + "/" + dir + "/" + "toa_b2dp.TIF")
    toa_b3dp.save(path + parentdir + "/" + dir + "/" + "toa_b3dp.TIF")
    toa_b4dp.save(path + parentdir + "/" + dir + "/" + "toa_b4dp.TIF")
    print "dpRasters have been created and saved as TIFS"

##        arcpy.CompositeBands_management(path + parentdir + "/" + dir + "/" + "Rt1"; path + parentdir + "/" + dir + "/" + "Rt2";
##        path + parentdir + "/" + dir + "/" + "Rt3"; path + parentdir + "/" + dir + "/" + "Rt4", L_bcomp)
##        L_bcomp.save(path + parentdir + "/" + dir + "/" + "L_bcomp")

    print "*************************************************************************"
    print "*** Calculating image statistics ***"
    print""
    bands = ("toa_b1.TIF", "toa_b2.TIF", "toa_b3.TIF", "toa_b4.TIF")
    rbands = ("toa_b1dp.TIF", "toa_b2dp.TIF", "toa_b3dp.TIF", "toa_b4dp.TIF")

    print "*************************************************************************"
    print "***Starting to Classify Urban area and Calculate Area Urban Sprawl***"
    print ""

    # Define Urban shapefile as variable, created by user for clipping out urban area
##    Urban_shp = arcpy.GetParameterAsText(0)
##    if Urban_shp == '#' or not Urban_shp:
##        Urban_shp = r"C:\\gisdata\\india\\imagery\\Urban.shp" # provide a default value if unspecified
    Urban_shp = "C:/gisdata/india/shapes/Urban.shp" # provide a default value if unspecified
##    Input_Rasters = arcpy.GetParameterAsText(1)
##    if Input_Rasters == '#' or not Input_Rasters:
    Input_Rasters = path + parentdir + "/" + dir + "/" + "toa_b1dp.TIF"; path + parentdir + "/" + dir + "/" + "toa_b2dp.TIF"; path + parentdir + "/" + dir + "/" + "toa_b3dp.TIF"; path + parentdir + "/" + dir + "/" + "toa_b4dp.TIF" # provide a default value if unspecified

    Dissolve_Field_s_ = arcpy.GetParameterAsText(2)
    if Dissolve_Field_s_ == '#' or not Dissolve_Field_s_:
        Dissolve_Field_s_ = "GRIDCODE;Name" # provide a default value if unspecified

    Output_signature_file = arcpy.GetParameterAsText(3)

##    # Local variables for classication:
##    Rt_CompositeBands_tif = Input_Rasters
##    Extract = Rt_CompositeBands.tif
##    isocluster = Extract.tif
##    isocluster_shp = isocluster
##    isocluster_Identity_shp = isocluster_shp
##    isocluster_Identity_Dissolve_shp = isocluster_Identity_shp
##    isocluster_Identity_Dissolv_Area_shp = isocluster_Identity_Dissolve_shp

    # Process: Composite Bands
    print "Process: Composite Bands"
##    arcpy.CompositeBands_management(Input_Rasters, "Rt_CompBands.tif")
    arcpy.CompositeBands_management(rbands, "GBG_CompBands.tif")

    # Process: Extract by Mask
    print "Process: Extract by Mask"
    arcpy.gp.ExtractByMask_sa("GBG_CompBands.tif", Urban_shp, "GBGextract.tif")

##    # Process: Iso Cluster Unsupervised Classification
##    print "Process: Iso Cluster Unsupervised Classification"
##    arcpy.gp.IsoClusterUnsupervisedClassification_sa(path + parentdir + "/" + dir + "/" + "Extract.tif", "5", "isocluster.tif", "20", "10", Output_signature_file)

    # Process: Maximum Likelihood Classification
    print "Process: Maximum Likelihood Classification"
    arcpy.gp.MLClassify_sa(path + parentdir + "/" + dir + "/" + "GBGextract.tif", path + parentdir + "/" + "extract.gsg", "isocluster.tif", "0.0", "EQUAL", "", "")


    # Process: Raster to Polygon
    print "Process: Raster to Polygon"
    arcpy.RasterToPolygon_conversion("isocluster.tif", "isocluster.shp", "SIMPLIFY", "VALUE")

    # Process: Identity
    print "Process: Identity"
    arcpy.Identity_analysis("isocluster.shp", Urban_shp, "isocluster_Identity.shp", "ALL", "", "NO_RELATIONSHIPS")

    # Process: Dissolve
    print "Process: Dissolve"
    arcpy.Dissolve_management("isocluster_Identity.shp", "isocluster_Identity_Dissolve.shp", Dissolve_Field_s_, "", "MULTI_PART", "DISSOLVE_LINES")

    # Process: Calculate Areas
    print "Process: Calculate Areas"
    arcpy.CalculateAreas_stats("isocluster_Identity_Dissolve.shp", "isocluster_Identity_Dissolv_Area.shp")
    print "starting next run"
    print ""

print "*************************************************************************"
print "Finished Processing!"
print "*************************************************************************"
