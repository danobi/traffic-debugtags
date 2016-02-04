#!/usr/bin/python
import sys
import subprocess
import re

def main():
  if len(sys.argv) < 2:
    print("Usage: ./traffic-debugtags source_dir")
  source_dir = sys.argv[1]

  # Run the unix `grep` command
  try:
    output = subprocess.check_output("grep -Ihr 'Debug(\"' {0}".format(source_dir), shell=True, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError, e:
    print("Some kind of error happened")
    print e.output
  
  # Parse results of `grep`
  tags = []
  lines = output.split('\n')
  for line in lines:
    line = line.strip()

    # Hueristic detection of debug statements
    # We only want the tags to `Debug()` functions
    if line[0:6] != "Debug(":
      continue

    # Find the two "'s and extract what's between them
    index1 = line.find('"', 0)
    index2 = line.find('"', index1+1)
    tag = line[index1+1:index2]
    if ' ' not in tag and tag not in tags:
      tags.append(tag)

  for tag in tags:
    print(tag)

if __name__ == '__main__':
  main()

