"""
The main module of DropChef.

This module provides the "baking" of markdown files & layout configurations
into a set of html files, suitable for serving.
"""
# Importing drochef.config needs a bit of song-and-dance when running from the
# command-line.
try:
  from . import config
except ValueError:
  import config

import os
import re
import subprocess

def bake(filePath, template=None):
  path = os.environ['PATH']
  for pathDir in path.split(':'):
    if os.path.exists(os.path.join(pathDir, 'multimarkdown')):
      mmdPath = os.path.join(pathDir, 'multimarkdown')
      break
  else:
    raise Exception("No multimarkdown in PATH")

  headerlessMarkdown = []
  headers = {}
  lineRe = re.compile(r'^(\w[^:]*):\s+(.*)$')
  with open(filePath, 'r') as markdownPost:
    inHeader = True
    for line in markdownPost:
      if inHeader:
        match = lineRe.match(line)
        if match:
          headers[match.group(1)] = match.group(2)
          continue
        else:
          inHeader = False
      headerlessMarkdown.append(line)
  headerlessMarkdown = '\n'.join(headerlessMarkdown)

  html = subprocess.Popen(
      [mmdPath, "-t", "html"],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE
  ).communicate(headerlessMarkdown)[0]
  template = open(template or config.postTemplate).read()
  return template.format(**{
    'content': html,
    'title': headers['Title'],
    'author': headers['Author'],
    'date': headers['Date']
  })

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 3:
    print bake(sys.argv[1], sys.argv[2])
