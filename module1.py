import os
import sys
import arcpy
#git add -A (for add all)
from arcpy import env
env.overwriteOutput = True

#change your feature class name here
fc_name = "TestGps"

current_dir = os.getcwd() 
fgdb_name = 'DataCollection.gdb'
workspace_path = current_dir + '\\' +fgdb_name

fc_path = workspace_path + '\\'  + fc_name
    
#SR Definition
SRDefinition="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-22041257.773878 -33265068.6042249 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"

#create a gdb
arcpy.CreateFileGDB_management(current_dir, fgdb_name)
    
# Create the coded value domains
# You can add additional domains below   
arcpy.CreateDomain_management(workspace_path, 'GNSSFixType', 'GNSSFixType', 'SHORT', 'CODED', 'DUPLICATE', 'DEFAULT')
arcpy.AddCodedValueToDomain_management(workspace_path, 'GNSSFixType', 0, 'Fix not valid')
arcpy.AddCodedValueToDomain_management(workspace_path, 'GNSSFixType', 1, 'GPS')
arcpy.AddCodedValueToDomain_management(workspace_path, 'GNSSFixType', 2, 'Differential GPS')
arcpy.AddCodedValueToDomain_management(workspace_path, 'GNSSFixType', 4, 'RTK Fixed')
arcpy.AddCodedValueToDomain_management(workspace_path, 'GNSSFixType', 5, 'RTK Float')

arcpy.CreateDomain_management(workspace_path, 'Conditions', 'Sky Conditions', 'SHORT', 'CODED', 'DUPLICATE', 'DEFAULT')
arcpy.AddCodedValueToDomain_management(workspace_path, 'Conditions', 1, 'open sky')
arcpy.AddCodedValueToDomain_management(workspace_path, 'Conditions', 2, 'partiallyobscurred<25%')
arcpy.AddCodedValueToDomain_management(workspace_path, 'Conditions', 3, 'marginallyobscurred<50%')
arcpy.AddCodedValueToDomain_management(workspace_path, 'Conditions', 4, 'highlyobscurred<75%')

arcpy.CreateDomain_management(workspace_path, "NumSatellites", "NumSatellites", "SHORT", "RANGE", "DEFAULT", "DEFAULT")
arcpy.SetValueForRangeDomain_management(workspace_path, "NumSatellites", 0, 99)

print('All done. Your fgdb was created at ' + workspace_path)
print('Your feature class is called ' + fc_name)


