from typing import List, Tuple
import re

import xml.etree.ElementTree as ET

Uncovered = Tuple[str, List[int]]


def get_line_numbers(class_node):
    uncovered = class_node.findall(".//line[@hits='0']")
    line_numbers = []
    for line in uncovered:
        line_numbers.append(int(line.attrib["number"]))
    return line_numbers


def get_uncovered(parsed_xml) -> List[Uncovered]:
    root = tree.getroot()
    result: List[Uncovered] = []
    classes = root.findall(".//class")
    for class_node in classes:
        filename = class_node.attrib["filename"]
        line_numbers = get_line_numbers(class_node)
        if len(line_numbers) > 0:
            result.append((filename, line_numbers))
    return result


def adjust_line(line: str) -> str:
    return f"# {line}"


def get_leading_space(line: str) -> str:
    pattern = r"^\s+"
    matched = re.match(pattern, line)
    if matched:
        return matched.group()
    return ""


def remove_uncovered(uncovered: List[Uncovered]):
    for filename, line_numbers in uncovered:
        with open(filename, "r", encoding="utf8") as file:
            lines = file.readlines()
            for n in line_numbers[::-1]:
                line_number_index = n - 1

                # use slice trick to insert a return right before
                original_line = lines[line_number_index]
                leading_space = get_leading_space(original_line)
                # lines[line_number_index : line_number_index + 1] = [
                lines[line_number_index] = f"# {original_line}"
                # f"{leading_space}return\n",
                # original_line,

        # print("".join(lines))
        with open(filename, "w", encoding="utf8") as file:
            file.writelines(lines)


tree = ET.parse("./coverage.xml")
uncovered = get_uncovered(tree)
remove_uncovered(uncovered)
