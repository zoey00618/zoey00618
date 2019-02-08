import os
import sys
import arcpy

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
    
arcpy.CreateDomain_management(workspace_path, "NumStationID", "NumStationID", "SHORT", "RANGE", "DEFAULT", "DEFAULT")
arcpy.SetValueForRangeDomain_management(workspace_path, "NumStationID", 0, 1023)
        
print('Done adding Domains')

#Create the Feature Class
arcpy.CreateFeatureclass_management(out_path=workspace_path
                                    , out_name=fc_name
                                    , geometry_type="POINT"
                                    , template=""
                                    , has_m="DISABLED"
                                    , has_z="DISABLED"
                                    , spatial_reference=SRDefinition
                                    , config_keyword=""
                                    , spatial_grid_1="0"
                                    , spatial_grid_2="0"
                                    , spatial_grid_3="0"
                                    )
print('Done creating feature class')
    
#add data field here
arcpy.AddField_management(fc_path,'FIELDNOTES','TEXT','','','500','Field Notes','NULLABLE','NON_REQUIRED','' )
    
#add GPS Metadata field information
arcpy.AddField_management(fc_path,'ESRIGNSS_RECEIVER','TEXT','','','50','Receiver Name','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_H_RMS','DOUBLE','','','','Horizontal Accuracy','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_V_RMS','DOUBLE','','','','Vertical Accuracy','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_LATITUDE','DOUBLE','','','','Latitude','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_LONGITUDE','DOUBLE','','','','Longitude','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_ALTITUDE','DOUBLE','','','','Altitude','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_PDOP','DOUBLE','','','','PDOP','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_HDOP','DOUBLE','','','','HDOP','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_VDOP','DOUBLE','','','','VDOP','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_FIXTYPE','SHORT','','','','Fix Type','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_CORRECTIONAGE','DOUBLE','','','','Correction Age','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_STATIONID','SHORT','','','','Station ID','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_NUMSATS','SHORT','','','','Number of Satellites','NULLABLE','NON_REQUIRED','' )
arcpy.AddField_management(fc_path,'ESRIGNSS_FIXDATETIME','DATE','','','','Fix Time','NULLABLE','NON_REQUIRED','' )
   
#assign field to domain
arcpy.AssignDomainToField_management( fc_path, 'ESRIGNSS_FIXTYPE', 'GNSSFixType')
arcpy.AssignDomainToField_management( fc_path, 'ESRIGNSS_STATIONID', 'NumStationID')
arcpy.AssignDomainToField_management( fc_path, 'ESRIGNSS_NUMSATS', 'NumSatellites')

print('Done adding field information')

print('All done. Your fgdb was created at ' + workspace_path)
print('Your feature class is called ' + fc_name)


