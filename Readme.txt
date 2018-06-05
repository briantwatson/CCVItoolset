CCVI Toolset - README!
======================
Warning
-------
This toolset is in the early stages of development.  	Please check that the results match those calculated manually. It is suggested the technician have a working knowledge of ArcGIS and familiarity with python.

Synopsis
--------
NatureServe has developed the Climate Change Vulnerability Index (CCVI) to rapidly assess vulnerability of animal and plant species to climate change using a scoring system based on predicted exposure and sensitivity to climate change.  The CCVI incorporates the overlay and classification of species ranges with both predicted and historical GIS climate data as factors of a species’ exposure and sensitivity to climate change.   The CCVI Toolset is a suite of tools that calculates exposure to predicted change in both moisture and temperature for single or multiple species in varying formats.

Rough scripts that were developed for historical factors of the CCVI (C2ai and C2bi, version 2.1) are included under the code folder.

These python scripts and ArcGIS tools were originally devloped to expedite CCVI assessments for a project in the [Kwit Lab](http://www.charleskwit.com/endangered-plants-and-climate-change-in-tennessee/) at The University of Tennessee.


About ArcGIS Script Tool
------------------------

In CCVI_Template.mxd, there is a toolbar with two tools, one for handling single vector polygon files (species ranges) with multiple species classified by values in a field.  The second handles situations where an individual file is already present for each species.  Note that the folder containing multiple files should contain nothing else besides those species range files.

The tool will generate a new file for each species under ../data/output/ProjectName/CCVIPredMois as well as /CCVIPredTemp, with ProjectName being the name of the project you entered in the tool.

Each raster file will be reclassified to a number associated with the CCVI 2.1 guidelines for predicted moisture and temperature. A percentage field is added with a calculated percentage for each class.  Below are the reclassification numbers for predicted moisture and temperature.

#####Predicted Moisture Reclassification Files:

| Original Value | Reclass Value |
| --- | --- |
| < -0.119 | 6 |
| -0.119 -- -0.097 | 5 |
| -0.096 -- -0.074 | 4 |
| -0.073 -- -0.051 | 3 |
| -0.050 -- -0.028 | 2 |
| > -0.028 | 1 |

#####Predicted Temp Reclassification:

| Original Value | Reclass Value |
| --- | --- | 
| > 5.5 | 5 |
| 5.1 -- 5.5 | 4 |
| 4.5 -- 5.0 | 3 |
| 3.9 -- 4.4 | 2 |
| < 3.9 | 1 |





