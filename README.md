This is the code for the site catchment analysis described further on [archaeoinformatics blog](http://archaeoinformatics.net/python-for-site-catchment-qgis/). This script calculates serveral site catchment analyses in one go: It takes a point layer of sites, draws a circle around them. Then it calculates for erery circle the areas of different polygons taken from another layer.

For more information please visit the link to the blogpost above.

# Setup

The first time, download this repository via `git clone https://github.com/PyQGISCologne/PyQGIS_Site_Catchment.git` and load `site_catchment-script.py` into your local QGIS [Python Console](https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/intro.html#scripting-in-the-python-console). Adjust variables with placeholders to your local enviroment (line 10 - 15).

After that load the code in Python-Konsole editor and run it.