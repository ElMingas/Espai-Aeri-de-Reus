from tkinter import messagebox

import xml.etree.ElementTree as ET
from xml.dom import minidom
import webbrowser
import os

def generate_reachability_kml(nav_points, segments, nodes_output_file, segs_output_file):
    if not nav_points or not segments:
        messagebox.showwarning("Warning", "You haven't selected any nodes yet. Please try again later")
        return

    # Generar KML para nodos
    reachability_nodes_kml(nav_points, nodes_output_file)
    # Generar KML para segmentos
    reachability_segs_kml(segments, segs_output_file)

def reachability_nodes_kml(nav_points, output_file):
    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')

    # Create placemarks for each navigation point
    for nav_point in nav_points:
        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = f"{nav_point.name} ({nav_point.number})"
        point = ET.SubElement(placemark, 'Point')
        ET.SubElement(point, 'coordinates').text = f"{nav_point.x},{nav_point.y},0"

    # Save KML file
    save_kml(kml, output_file)

def reachability_segs_kml(segments, output_file):
    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')

    # Create placemarks for each segment
    for seg in segments:
        origin, dest = seg.origin, seg.destination
        origin_id, dest_id = origin.number, dest.number

        if origin and dest:
            placemark = ET.SubElement(document, 'Placemark')
            ET.SubElement(placemark, 'name').text = f"Segment {origin_id}-{dest_id}"

            linestring = ET.SubElement(placemark, 'LineString')
            ET.SubElement(linestring, 'altitudeMode').text = 'clampToGround'
            ET.SubElement(linestring, 'extrude').text = '1'
            ET.SubElement(linestring, 'tessellate').text = '1'
            ET.SubElement(linestring, 'coordinates').text = (
                f"{origin.x},{origin.y},0 "
                f"{dest.x},{dest.y},0"
            )

    # Save KML file
    save_kml(kml, output_file)
def save_kml(kml_element, output_file):
    rough_string = ET.tostring(kml_element)
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml()

    try:
        with open(output_file, 'w') as f:
            f.write(pretty_xml)
        webbrowser.open(os.path.abspath(output_file))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save/open KML: {str(e)}")


def txt_to_kml_path(opt_path, output_file):
    if opt_path is None:
        messagebox.showwarning("Warning", "No optimal route calculated")
        return

    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')


    for nav_point in opt_path:
        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = f"{nav_point.name} ({nav_point.number})"
        point = ET.SubElement(placemark, 'Point')
        ET.SubElement(point, 'coordinates').text = f"{nav_point.x},{nav_point.y},0"

    # Añadir la ruta completa
    route_placemark = ET.SubElement(document, 'Placemark')
    ET.SubElement(route_placemark, 'name').text = "Optimal Route"
    ET.SubElement(route_placemark, 'description').text = f"Route with {len(opt_path)} navigation points"

    linestring = ET.SubElement(route_placemark, 'LineString')
    ET.SubElement(linestring, 'altitudeMode').text = 'clampToGround'
    ET.SubElement(linestring, 'extrude').text = '1'
    ET.SubElement(linestring, 'tessellate').text = '1'

    # Generar coordenadas
    coordinates_text = ' '.join(f"{p.x},{p.y},0" for p in opt_path)
    ET.SubElement(linestring, 'coordinates').text = coordinates_text

    try:
        rough_string = ET.tostring(kml, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        abs_path = os.path.abspath(output_file)
        webbrowser.open(abs_path)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate KML: {str(e)}")