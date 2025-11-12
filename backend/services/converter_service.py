import json
import xml.etree.ElementTree as ET
import xmltodict

def xml_to_json(xml_string: str) -> str:
    """Convert XML to JSON"""
    try:
        # Parse XML and convert to dict
        data_dict = xmltodict.parse(xml_string)
        # Convert dict to JSON with pretty formatting
        json_output = json.dumps(data_dict, indent=2)
        return json_output
    except Exception as e:
        raise ValueError(f"Invalid XML: {str(e)}")

def json_to_xml(json_string: str) -> str:
    """Convert JSON to XML"""
    try:
        # Parse JSON string to dict
        data_dict = json.loads(json_string)
        # Convert dict to XML
        xml_output = xmltodict.unparse(data_dict, pretty=True)
        return xml_output
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise ValueError(f"Conversion error: {str(e)}")