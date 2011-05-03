from dropchef import config
from dropchef import sync
import Queue
import functools
import os
import tempfile
import threading
import time
import unittest

class TestSync(unittest.TestCase):
  """Unit test for sync module."""

  def test_watch(self):
    tmpDir = tempfile.mkdtemp()
    cmdQ = Queue.Queue()
    newFiles = Queue.Queue()
    def handler(newPath): newFiles.put(newPath)
    t = threading.Thread(target=sync.watch, args=[tmpDir, handler, cmdQ])
    toAdd = map(functools.partial(os.path.join, tmpDir),
        ['foo', 'bar', 'baz', 'quux'])
    t.start()
    for f in toAdd: open(f, 'w').close()
    cmdQ.put(config._STOP)
    cmdQ.join()
    t.join()
    notifications = list()
    while True:
      try:
        notifications.append(newFiles.get_nowait())
      except Queue.Empty:
        break
    self.assertEqual(sorted(notifications), sorted(toAdd))
    for f in toAdd:
      os.remove(f)
    os.rmdir(tmpDir)
