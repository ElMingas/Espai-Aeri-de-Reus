from tkinter import messagebox

import xml.etree.ElementTree as ET
from xml.dom import minidom
import webbrowser
import os

def txt_to_kml_neighbors(input_node, output_file):
    if not input_node:
        messagebox.showwarning("Warning", "You haven't selected any nodes yet. Please try again later")
        return
    elif not input_node.neighbors:
        messagebox.showwarning("Warning", "The selected node has no neighbors")
        return

    kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = ET.SubElement(kml, 'Document')

    style = ET.SubElement(document, 'Style', id='neighbor_style')
    line_style = ET.SubElement(style, 'LineStyle')
    ET.SubElement(line_style, 'color').text = 'ff00aaff'  # Azul claro (formato AABBGGRR)
    ET.SubElement(line_style, 'width').text = '2'

    # Punto principal
    main_placemark = ET.SubElement(document, 'Placemark')
    ET.SubElement(main_placemark, 'name').text = f"{input_node.name} ({input_node.number})"
    main_point = ET.SubElement(main_placemark, 'Point')
    ET.SubElement(main_point, 'coordinates').text = f"{input_node.x},{input_node.y},0"

    # Puntos vecinos
    for neighbor in input_node.neighbors:
        neighbor_placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(neighbor_placemark, 'name').text = f"{neighbor.name} ({neighbor.number})"
        neighbor_point = ET.SubElement(neighbor_placemark, 'Point')
        ET.SubElement(neighbor_point, 'coordinates').text = f"{neighbor.x},{neighbor.y},0"

        segment_placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(segment_placemark, 'name').text = f"Connection {input_node.number}-{neighbor.number}"
        ET.SubElement(segment_placemark, 'styleUrl').text = '#neighbor_style'

        linestring = ET.SubElement(segment_placemark, 'LineString')
        ET.SubElement(linestring, 'altitudeMode').text = 'clampToGround'
        ET.SubElement(linestring, 'coordinates').text = (
            f"{input_node.x},{input_node.y},0 "
            f"{neighbor.x},{neighbor.y},0"
        )

    try:
        rough_string = ET.tostring(kml, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        webbrowser.open(os.path.abspath(output_file))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate KML: {str(e)}")