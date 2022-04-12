from datetime import datetime
import sys
import pathlib
from tkinter import W
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
    files_to_fix = 0
    lines_to_fix = 0
    for class_node in classes:
        filename = class_node.attrib["filename"]
        line_numbers = get_line_numbers(class_node)
        if len(line_numbers) > 0:
            files_to_fix += 1
            lines_to_fix += len(line_numbers)
            result.append((filename, line_numbers))
    print(f"need cover: {files_to_fix} files, {lines_to_fix} lines")
    return result


def adjust_line(line: str) -> str:
    return f"# uncovered -> {line}"


def get_leading_space(line: str) -> str:
    pattern = r"^\s+"
    matched = re.match(pattern, line)
    if matched:
        return matched.group()
    return ""


def remove_uncovered(uncovered: List[Uncovered], warn_only=False):
    for filename, line_numbers in uncovered:
        # fixed_filename = f"src/{filename}"
        fixed_filename = filename
        with open(fixed_filename, "r", encoding="utf8") as file:
            lines = file.readlines()
            for n in line_numbers[::-1]:
                line_number_index = n - 1
                # use slice trick to insert a return right before
                original_line = lines[line_number_index]
                leading_space = get_leading_space(original_line)
                # lines[line_number_index : line_number_index + 1] = [
                lines[line_number_index] = adjust_line(original_line)
                # f"{leading_space}return\n",
                # original_line,
        # print("".join(lines))
        if warn_only:
            print(fixed_filename)
            print(line_numbers)
        else:
            with open(filename, "w", encoding="utf8") as file:
                file.writelines(lines)


def time_to_int():
    pass


def get_last_run() -> int:
    last_run_path = pathlib.Path("./last_run")
    try:
        with open(last_run_path, "r") as f:
            text = f.read()
            if text == "":
                return None
            return int(text)
    except FileNotFoundError:
        return None


def set_last_run(value: int) -> None:
    last_run_path = pathlib.Path("./last_run")
    with open(last_run_path, "w") as f:
        f.write(str(value))


def get_run_time_from_coverage_file(coverage_file_path: pathlib.Path) -> int:
    if coverage_file_path.exists():
        modifed = coverage_file_path.stat().st_mtime
        return int(modifed)
    else:
        raise Exception("Why is this running without a coverage file?")


exit_code = sys.argv[1]
if exit_code != "0":
    # We get a code when pytest fails.  If it's green, we'll get '0'.
    # Don't try to clean up code until we're green.
    sys.exit(1)

previous_coverage_ts = get_last_run()

coverage_file_path = pathlib.Path("./coverage.xml")
coverage_timestamp = get_run_time_from_coverage_file(coverage_file_path)
should_run = previous_coverage_ts is None or previous_coverage_ts < coverage_timestamp


if should_run:
    tree = ET.parse(coverage_file_path)
    uncovered = get_uncovered(tree)
    remove_uncovered(uncovered, warn_only=False)
    set_last_run(coverage_timestamp)
else:
    # print(
    #     f"previous_coverage_ts {previous_coverage_ts}, coverage_timestamp {coverage_timestamp}"
    # )
    print("no coverage changes")
    sys.exit(1)
