from dropchef import config
from dropchef import bake
import os
import tempfile
import unittest

class TestBake(unittest.TestCase):
  """Unit test for bake module."""

  def test_bake(self):
    tmpFd, tmpFn = tempfile.mkstemp(text=True)
    os.write(tmpFd, '\n'.join([
        "Title: Test",
        "Author: Tester",
        "Date: 8 May 2011",
        "",
        "# Foo #",
        "",
        "Jackdaws love my big sphinx of quartz"
      ])
    )
    os.close(tmpFd)

    templateFd, testTemplate = tempfile.mkstemp(text=True)
    template = '\n'.join([
        "<!DOCTYPE html>",
        "<html>",
          "<head><title>{title}</title></head>",
          "<body>",
            "<section>",
              "<h1>{title}</h1>",
              "<h2>By {author} on {date}</h2>",
              "{content}",
            "</section>",
          "</body>",
        "</html>"
    ])
    os.write(templateFd, template)
    os.close(templateFd)

    baked = bake.bake(tmpFn, testTemplate)

    self.assertEqual(baked, template.format(
      title='Test', author='Tester', date='8 May 2011',
      content=(
        "<h1 id=\"foo\">Foo</h1>\n\n"
        "<p>Jackdaws love my big sphinx of quartz</p>\n")
      )
    )

    os.remove(tmpFn)
    os.remove(testTemplate)

