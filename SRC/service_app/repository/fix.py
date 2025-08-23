#!/usr/bin/env python
# convert optional class members in BaseModel classes to have a default value of None
import argparse
import re
import sys


def add_optional_none(path):
  with open(path, 'r') as file:
    content = file.readlines()
  lines = []
  lines.append("# Default value None added to Optional class members by fix.py\n")
  in_base_model_class = False
  for i, line in enumerate(content):
    modified_line = None
    class_match = re.match(r'class (\w+)\((\w+\.)?BaseModel\):', line)
    if class_match:
      in_base_model_class = True
    if in_base_model_class:
      optional_match = re.match(r'^(\s+\w+:\s*Optional\[.*\])\s*\n$', line)
      if optional_match:
        modified_line = f"{optional_match.group(1)} = None\n"
    if modified_line is None:
      lines.append(line)
    else:
      lines.append(modified_line)
    if in_base_model_class and line.strip() == '':
      in_base_model_class = False
  with open(path, 'w') as file:
    file.writelines(lines)


def main():
  parser = argparse.ArgumentParser("fix.py")
  parser.add_argument('files', nargs='*', help="List of files to modify")
  args = parser.parse_args()
  for path in args.files:
    try:
      add_optional_none(path)
    except FileNotFoundError:
      print(f"{path} not found")
      sys.exit(1)
    except Exception as err:
      print(f"error occurred while reading {path}: {err}")
      sys.exit(1)


if __name__ == "__main__":
  main()
