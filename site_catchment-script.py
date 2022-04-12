# Title: Site Catchment Analysis - A scripted PyQGIS solution
# Authors: Sophie Schmidt, Sara Schiesberg, Kai Vogl, Sandra Rung
# Objective: Takes a point and a polygon layer. Returns a table giving percentages for polygon types around each point.  

# Import libraries 
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorFileWriter

# Insert values
land = 'INSERT_YOUR_ABSOLUT_PATH_TO_POLYGON_LAYER'
land_id = 'INSERT_ID´S NAME'
samp = 'INSERT_YOUR_ABSOLUT_PATH_TO_POINT_LAYER'
samp_id = 'INSERT_ID´S NAME'
output = 'INSERT_YOUR_ABSOLUT_PATH_TO_CSV_LAYER'
radius = 'INSERT NUMBER'

# Add point and polygon layers to QGIS
landuse = iface.addVectorLayer(land, 'landuse', 'ogr')
samples = iface.addVectorLayer(samp, 'sample', 'ogr')

# Create a new layer for results
result = QgsVectorLayer('Point?crs=EPSG:32628', 'Result', 'memory')
prov = result.dataProvider()
prov.addAttributes([QgsField('id', QVariant.Int), QgsField('obj', QVariant.String), QgsField('area', QVariant.Double), QgsField('area%', QVariant.Double)])
result.updateFields()
fields = prov.fields()

# Nested loop iterating for every point over all polygons
feats = []
for sample in samples.getFeatures():
    for poly in landuse.getFeatures():
        puffer = sample.geometry().buffer(radius, 25) # buffer with 25 segments boundary
        part = puffer.intersection(poly.geometry())
        feat = QgsFeature(fields) 
        feat.setGeometry(sample.geometry())
        feat['id'] = sample[samp_id]
        feat ['obj'] = poly[land_id]
        feat['area'] = part.area()
        if feat ['area'] > 0:
            feat['area%'] = (part.area())/(puffer.area())
            feats.append(feat)

# Add the feat
prov.addFeatures(feats)
QgsProject.instance().addMapLayer(result)

# Save the results as .csv
QgsVectorFileWriter.writeAsVectorFormat(result, output,'UTF-8', 
result.crs(), 'CSV')

