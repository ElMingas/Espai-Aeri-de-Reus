import xml.etree.ElementTree as ET
from xml.dom import minidom
import webbrowser
import os

def txt_to_kml(input_nodes, input_segs, output_file):
    # Crear la estructura básica del KML
    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')

    # Leer el archivo de entrada y almacenar puntos
    for nav_point in input_nodes:
        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = f"{nav_point.name} ({nav_point.number})"
        point = ET.SubElement(placemark, 'Point')
        ET.SubElement(point, 'coordinates').text = f"{nav_point.x},{nav_point.y},0"

    # Generar y guardar el KML de puntos
    with open(output_file, 'w') as f:
        f.write(minidom.parseString(ET.tostring(kml)).toprettyxml())

    # Generar KML de segmentos
    txt_to_kml_segments(input_segs,'nav_seg.kml')

    # Abrir ambos KMLs
    try:
        webbrowser.open(os.path.abspath(output_file))
        webbrowser.open(os.path.abspath('nav_seg.kml'))
    except Exception as e:
        print(f"Error al abrir archivos KML: {e}")
def txt_to_kml_segments(input_segs, output_file):
    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')

    for seg in input_segs:
        origin, dest = seg.origin, seg.destination

        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = f"{origin.name} to {dest.name}"

        linestring = ET.SubElement(placemark, 'LineString')
        ET.SubElement(linestring, 'altitudeMode').text = 'clampToGround'
        ET.SubElement(linestring, 'extrude').text = '1'
        ET.SubElement(linestring, 'tessellate').text = '1'
        ET.SubElement(linestring, 'coordinates').text = (
            f"{origin.x},{origin.y},0 "
            f"{dest.x},{dest.y},0"
        )

    with open(output_file, 'w') as f:
        f.write(minidom.parseString(ET.tostring(kml)).toprettyxml())

#txt_to_kml(r'catalonia\Cat_nav.txt', 'nav_points.kml')