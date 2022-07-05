# Title: Site Catchment Analysis - A scripted PyQGIS solution
# Authors: Sophie Schmidt, Sara Schiesberg, Kai Vogl, Sandra Rung
# License: MIT (https://opensource.org/licenses/mit-license.php)
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
radius = 'INSERT NUMBER' # this needs to be a number, therefore don't use ' ' !

# Add point and polygon layers to QGIS
landuse = iface.addVectorLayer(land, 'landuse', 'ogr')
samples = iface.addVectorLayer(samp, 'sample', 'ogr')

# Create a new layer for results
result = QgsVectorLayer('Point?crs=' + samples.crs().authid(), 'Result', 'memory')
prov = result.dataProvider()
prov.addAttributes([QgsField('id', QVariant.Int), QgsField('obj', QVariant.String), QgsField('area', QVariant.Double), QgsField('area%', QVariant.Double)])
result.updateFields()
fields = prov.fields()

# Nested loop iterating for every point over all polygons, inspired by: https://www.researchgate.net/post/How-to-calculate-the-intersected-area-from-a-layer-with-overlapping-buffers-in-qgis , see answer by Detlev Neumann
feats = []
for sample in samples.getFeatures():
    puffer = sample.geometry().buffer(radius, 25) # buffer with 25 segments boundary
    for poly in landuse.getFeatures():
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

