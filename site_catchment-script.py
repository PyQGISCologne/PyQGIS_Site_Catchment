#******************************************************************************************************************************************************
# Puffer; Flächenanteile pro Punkt # 
#***********************************************************************************************************************************

# Dateneingabe: Pfade
samp = "/home/sophie/ownCloud/PyQGIS/P2_Puffer_Daten/QPy_Site_Catchment/AtlantGIS_data/archaeological_sites.shp"
land = "/home/sophie/ownCloud/PyQGIS/P2_Puffer_Daten/QPy_Site_Catchment/AtlantGIS_data/landtype.shp"

# Als Karte laden, addVectorLayer() gibt einen QgsVectorLayer aus mit dem man arbeiten kann
samples = iface.addVectorLayer(samp, "sample", "ogr")
landuse = iface.addVectorLayer(land, "landuse", "ogr")

# Ein neuer Vektorlayer wird erstellt (ergebnis)
from qgis.PyQt.QtCore import QVariant
result = QgsVectorLayer("Point?crs=EPSG:5678", "Result", "memory")
prov = result.dataProvider()

# Diesem Layer werden variablen hinzugefügt
prov.addAttributes([QgsField("id", QVariant.Int), QgsField("obj", QVariant.String), 
QgsField("area", QVariant.Double), QgsField("area%", QVariant.Double)])
result.updateFields() # tell the vector layer to fetch changes from the provider
fields = prov.fields()

# Eine leere Liste wird erstellt
feats = []
boden = landuse.getFeatures()

# Die Schleife erzeugt für jeden Punkt alle Zeilen aus der Bodentabelle
for sample in samples.getFeatures():
    for poly in landuse.getFeatures():
        # 100 units buffer with a 25 segments boundary, es wird ein obj. "qgis._core.QgsGeometry" erzeugt
        puffer = sample.geometry().buffer(100, 25)
        part = puffer.intersection(poly.geometry())
        feat = QgsFeature(fields) # es wird ein objekt "qgis._core.QgsFeature" erzeugt 
        feat.setGeometry(sample.geometry()) # den features werden die geometrien der samples zugewiesen
        feat['id'] = sample["ID_AR_SITE"]
        feat ['obj'] = poly["Landtype"]
        feat['area'] = part.area()
        if feat['area'] > 0:
            feat['area%'] = (part.area())/(puffer.area())
            feats.append(feat)
prov.addFeatures(feats) # hier wird dem provider des result-layers die daten zugewiesen

QgsProject.instance().addMapLayer(result)

# Alle leeren Zeilen löschen
#caps = result.dataProvider().capabilities()
bod = result.getFeatures()
#dfeats = []

#for feat in bod: 
#   if feat ["area"]==0:
#        dfeats.append(feat.id())

#res = result.dataProvider().deleteFeatures(dfeats)
# QgsProject.instance().addMapLayer(result)

# Den Datensatz als csv exportieren
from qgis.core import QgsVectorFileWriter
QgsVectorFileWriter.writeAsVectorFormat(result, "/home/sophie/ownCloud/PyQGIS/P2_Puffer_Daten/QPy_Site_Catchment/AtlantGIS_data/result.csv","UTF-8", 
result.crs(), "CSV")

# Pandas
import pandas as pd
import numpy as np
tabelle = pd.read_csv("/home/sophie/ownCloud/PyQGIS/P2_Puffer_Daten/QPy_Site_Catchment/AtlantGIS_data/result.csv")
kreuztabelle = pd.pivot_table (tabelle, values='area%', index=['id'],columns=['obj'], aggfunc=np.sum)

