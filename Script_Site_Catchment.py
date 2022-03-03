# buffer script 
# Sara Schiesberg, Sophie Schmidt, Sandra Rung, Kai Vogl

# imports
#import os
import pandas as pd
import numpy as np
#from PyQt5.QtGui import *
#from qgis.core import QgsVectorLayer #Kai fragen, brauchen wir das?


from PyQt4.QtGui import QDialog, QFormLayout
from qgis.gui import *

qid = QInputDialog()

new_dialog = QDialog()

# erst alle input dialoge definieren, später zusammenführen
sites_pathInput = QInputDialog.getText(qid, "Path to archaeological point data", "Please enter the path to your shape file of archaeological data")
soils_pathInput = QInputDialog.getText(qid, "Path to soil polygon data", "Please enter the path to your shape file of soil data:")

segmentsInput = QInputDialog.getInt(qid, "Number of segments","Enter number of segments:")
radiusInput = QInputDialog.getInt(qid, "Puffer radius", "How large should the puffer radius be?:")
out_pathInput = QInputDialog.getText(qid, "Please enter where you want to save the output csv", "Path to output csv:")


# diese alle in ein QInput-widget
layout = QFormLayout()
layout.addWidget(sites_pathInput)
# combobox auswahl IDs
layout.addWidget(soils_pathInput)
# combobox auswahl spalte
layout.addWidget(radiusInput)
layout.addWidget(segmentsInput)
layout.addWidget(out_pathInput)


new_dialog.setLayout(layout)
new_dialog.show()  # To see possibility of this component, you need at least a layer opened



segmentsInput = QInputDialog.getInt(qid, "Number of segments","Enter number of segments:")

radius = radiusInput[0]
segments = segmentsInput[0]

sites_pathInput = QInputDialog.getText(qid, "Path to archaeological point data", "Please enter the path to your shape file of archaeological data")



sites_path = sites_pathInput[0]
sites = QgsVectorLayer(sites_path, "Sites", "ogr")
QgsProject.instance().addMapLayer(sites)

# Which of the following layers is the one with ID... 

# select the relevant field name

## geklaut von: https://webgeodatavore.github.io/pyqgis-samples/gui-group/QgsMapLayerComboBox.html

# Create dialog
new_dialog = QDialog()

# Add combobox for layer and field
map_layer_combo_box = QgsMapLayerComboBox()
map_layer_combo_box.setCurrentIndex(-1)
map_layer_combo_box.setFilters(QgsMapLayerProxyModel.VectorLayer)
field_combo_box = QgsFieldComboBox()

# Create a form layout and add the two combobox
layout = QFormLayout()
layout.addWidget(map_layer_combo_box)
layout.addWidget(field_combo_box)

# Add signal event
map_layer_combo_box.layerChanged.connect(field_combo_box.setLayer)  # setLayer is a native slot function


def on_field_changed(fieldName):
    print(fieldName)
    print("Layer field changed")

field_combo_box.fieldChanged.connect(on_field_changed)

new_dialog.setLayout(layout)
new_dialog.show()  # To see possibility of this component, you need at least a layer opened

###selber probieren

field_combo_box = QgsFieldComboBox()


si_names = []
for field in sites.fields():
    si_names.append(field.name())
    
for name in si_names:
    countryCombo.addItem(name)

soils_path = soils_pathInput[0]
soils = QgsVectorLayer(soils_path, "Soils", "ogr")
QgsProject.instance().addMapLayer(soils)

so_names = []
for field in soils.fields():
    so_names.append(field.name())

## input via combobox??
#include <qgsmaplayercombobox.h>
my_combo_box
my_combo_box.addItem(layer_name, layer_object)


out_pathInput = QInputDialog.getText(qid, "Please enter where you want to save the output csv", "Path to output csv:")
out = out_pathInput[0]

#sites = iface.addVectorLayer(sites_path, "Sites", "ogr")
#soils = iface.addVectorLayer(soils_path, "Soils", "ogr")

# needed lists
feats = []
buffers = []

for site in sites.getFeatures():
    for soil in soils.getFeatures():
        buffer = sites.geometry().buffer(radius, segments) #hier noch das als vektorlayer bauen? mit append?, nur so visualisieren, dass der user am ende entscheiden kann, ob er die Karte speichert. 
        part = puffer.intersection(soil.geometry())
        feat = QgsFeature(fields)
        feat.setGeometry(sites.geometry()) # den features werden die geometrien der samples zugewiesen
        feat['id'] = site["ID COLUMN of SITES DATA"]
        feat["obj"] = soil["VARIABLE YOU ASK FOR"]
        feat['area'] = part.area()
        feat['area%'] = (part.area())/(buffer.area())
        buffers.append(buffer) #check!
        if feat ["area"] !=0:
            feats.append(feat)

df = pd.DataFrame(feats, columns =['id', 'obj', 'area', 'area%'], dtype = float)
crosstable = pd.pivot_table (df, values='area%', index=['id'],columns=['obj'], aggfunc=np.sum)
crosstable.to_csv(out) 