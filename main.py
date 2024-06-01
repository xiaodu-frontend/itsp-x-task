import ast
import xml.etree.ElementTree as ET


class PythonSrcMlParser:
    def parse_to_xml(self, code):
        # Parse the code into an AST
        tree = ast.parse(code)

        # Convert the AST into XML
        xml_tree = self.ast_to_xml(tree)

        # Return a string of the XML
        return ET.tostring(xml_tree, encoding='unicode')

    def ast_to_xml(self, node):
        # Create an XML element with the node's class name
        xml_node = ET.Element(node.__class__.__name__)

        # Convert each field of the node into a child element
        for field in ast.iter_fields(node):
            field_name, field_value = field
            if isinstance(field_value, ast.AST):
                xml_node.append(self.ast_to_xml(field_value))
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, ast.AST):
                        xml_node.append(self.ast_to_xml(item))
            else:
                ET.SubElement(xml_node, field_name).text = str(field_value)

        return xml_node


if __name__ == '__main__':
    parser = PythonSrcMlParser()

    with open('example.py', 'r') as file:
        code = file.read()

    print(parser.parse_to_xml(code))
