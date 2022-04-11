from typing import List, Tuple
import xml.etree.ElementTree as ET
tree = ET.parse('./coverage.xml')

def get_line_numbers(class_node):
    uncovered = class_node.findall(".//line[@hits='0']")
    line_numbers = []
    for line in uncovered:
        line_numbers.append(int(line.attrib['number']))
    return line_numbers

def get_uncovered(parsed_xml) -> List[Tuple[str, List[int]]]:
    """
    returns List[(file_path, List[line_number])]
    """
    root = tree.getroot()
    result: List[Tuple[str, List[int]]] = []

    classes = root.findall(".//class")
    for class_node in classes:
        filename = class_node.attrib['filename']
        line_numbers = get_line_numbers(class_node)
        if len(line_numbers) > 0:
            result.append((filename, line_numbers))

    return result


def remove_uncovered(uncovered):
    # for each file
    for filename in uncovered:
        print(filename)
        # open the file (for reading and writing)
        with open(filename, 'rw') as file:
            print(file)
        # read lines
        # prepend each line (from back to start)
        # write file


uncovered = get_uncovered(tree)
remove_uncovered(uncovered)
