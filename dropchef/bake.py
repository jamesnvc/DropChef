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
  """Bake the (multi)markdown post located at `filePath` into HTML.

  Note that this requires multimarkdown be installed and on the $PATH. The
  converted entry will be baked into the HTML template provided for posts. This
  is done simply using python's builtin string.format method. The format method
  will be called with a dictionary containing the (HTML) content of the post at
  the 'content' key and all of the multimarkdown headers, camelCased.

  Args:
    - filePath: The path of the multimarkdown file to bake.
    - template: The location of the HTML template. If not given, defaults to
                dropbox.cnofig.postTemplate.
  Returns:
    - A string containing the processed HTML for the post.
  """
  path = os.environ['PATH']
  for pathDir in path.split(':'):
    if os.path.exists(os.path.join(pathDir, 'multimarkdown')):
      mmdPath = os.path.join(pathDir, 'multimarkdown')
      break
  else:
    raise Exception("No multimarkdown in PATH")

  def squeeze(s): return ''.join(s.split())
  def camelCase(s):
    return s[0].lower() + squeeze(s[1:])

  headerlessMarkdown = []
  headers = dict()
  lineRe = re.compile(r'^(\w[^:]*):\s+(.*)$')

  with open(filePath, 'r') as markdownPost:
    inHeader = True
    for line in markdownPost:
      if inHeader:
        match = lineRe.match(line)
        if match:
          headers[camelCase(match.group(1))] = match.group(2)
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
  templateVars = {'content': html}
  templateVars.update(headers)
  return template.format(**templateVars)

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 3:
    print bake(sys.argv[1], sys.argv[2])
