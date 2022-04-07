# Title: Site Catchment Analysis - A scripted PyQGIS solution
# Authors: Sophie Schmidt, Sara Schiesberg, Kai Vogl, Sandra Rung
# Objective: Takes a point and a polygon layer. Returns a table giving probabilities for polygon types around each point.  

# Import libraries 
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorFileWriter

# Enter paths to your data
land = "INSERT_YOUR_ABSOLUT_PATH_TO_POLYGON_LAYER"
samp = "INSERT_YOUR_ABSOLUT_PATH_TO_POLYGON_LAYER"

# Add the new vector layers to QGIS
landuse = iface.addVectorLayer(land, "landuse", "ogr")
samples = iface.addVectorLayer(samp, "sample", "ogr")

# Create a new layer for results
result = QgsVectorLayer("Point?crs=EPSG:32628", "Result", "memory")
prov = result.dataProvider()
prov.addAttributes([QgsField("id", QVariant.Int), QgsField("obj", QVariant.String), QgsField("area", QVariant.Double), QgsField("area%", QVariant.Double)])
result.updateFields()
fields = prov.fields()

# Nested loop iterating for every point over all polygons
feats = []
for sample in samples.getFeatures():
    for poly in landuse.getFeatures():
        puffer = sample.geometry().buffer(100, 25) # buffer with 100 units and a 25 segments boundary
        part = puffer.intersection(poly.geometry())
        feat = QgsFeature(fields) 
        feat.setGeometry(sample.geometry())
        feat['id'] = sample["ID_AR_SITE"]
        feat ["obj"] = poly["Landtype"]
        feat['area'] = part.area()
        if feat ["area"] > 0:
            feat['area%'] = (part.area())/(puffer.area())
            feats.append(feat)

# Add the feat
prov.addFeatures(feats)
QgsProject.instance().addMapLayer(result)

# Save the results as .csv
QgsVectorFileWriter.writeAsVectorFormat(result, "INSERT_YOUR_ABSOLUT_PATH_TO_POLYGON_LAYER","UTF-8", 
result.crs(), "CSV")

