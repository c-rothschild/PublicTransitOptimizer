from fastkml import KML
from fastkml import Placemark, Point, StyleUrl, Style
from fastkml.utils import find, find_all
import os

k = KML.parse("data/doc.kml")

placemarks = list(find_all(k, of_type=Placemark))

print(len(placemarks))