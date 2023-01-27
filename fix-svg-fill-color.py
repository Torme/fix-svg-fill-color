#!/usr/bin/env python3

import argparse
import os
import re
import sys
import readline

def fix_stroke(path: str, args: argparse.Namespace) -> None:
  root, ext = os.path.splitext(path)

  match = re.match(r'\.(svg|SVG)$', ext)
  if match:
    with open(path, 'r') as f:
      lines = f.readlines()

    for index, line in enumerate(lines):
      matchStroke = re.match(r'(<path (.*) stroke=(.*))/>$', line)
      matchFill = re.match(r'(.*)fill=(.*)', line)
      if matchStroke and not matchFill:
        lines[index] = f'{matchStroke[1]} fill="{args.color}" fill-opacity="0"/>\n'

    with open(path, 'w') as f:
      f.writelines(lines)


def process_path(path: str, args: argparse.Namespace) -> None:
  if os.path.isfile(path):
    fix_stroke(path, args)
  elif os.path.isdir(path):
    for entry in os.listdir(path):
      if entry == '.' or entry == '..':
        continue
      elif os.path.isfile(os.path.join(path, entry)):
        fix_stroke(path, args)
      elif args.recursive and os.path.isdir(os.path.join(path, entry)):
        process_path(os.path.join(path, entry), args)


def main() -> int:
  parser = argparse.ArgumentParser(description='Adds fill property to path with only stroke property in a svg files.')
  parser.add_argument('-r', '-R', '--recursive', action='store_true', help='process subdirectory recursively')
  parser.add_argument('-c', '--color', nargs='?', default='white', help='color used to fill the svg (with opacity 0)')
  parser.add_argument('paths', metavar='path', nargs='+', help='file or directory to process')

  args = parser.parse_args()

  for path in args.paths:
    process_path(path, args)
  return 0


if __name__ == '__main__':
  sys.exit(main())