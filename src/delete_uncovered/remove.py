from typing import List, Tuple
import xml.etree.ElementTree as ET
tree = ET.parse('./coverage.xml')

def get_line_numbers(class_node):
    uncovered = class_node.findall(".//line[@hits='0']")
    line_numbers = []
    for line in uncovered:
        line_numbers.append(int(line.attrib['number']))
    return line_numbers

Uncovered = Tuple[str, List[int]]

def get_uncovered(parsed_xml) -> List[Uncovered]:
    root = tree.getroot()
    result: List[Uncovered] = []

    classes = root.findall(".//class")
    for class_node in classes:
        filename = class_node.attrib['filename']
        line_numbers = get_line_numbers(class_node)
        if len(line_numbers) > 0:
            result.append((filename, line_numbers))

    return result

def adjust_line(line: str) -> str:
    return f'# {line}'

def remove_uncovered(uncovered: List[Uncovered]):
    for filename, line_numbers in uncovered:
        with open(filename, 'r', encoding='utf8') as file:
            lines = file.readlines()
            # TODO: go backward
            for n in line_numbers:
                lines[n - 1] = adjust_line(lines[n - 1])

        with open(filename, 'w', encoding='utf8') as file:
            file.writelines(lines)


uncovered = get_uncovered(tree)
remove_uncovered(uncovered)
