"""
Module for synchronizing & watching for updates.
"""
# Importing drochef.config needs a bit of song-and-dance when running from the
# command-line.
try:
  from . import config
except ValueError:
  import config

import time
import os
from watchdog import events
from watchdog import observers

class CreatedFileHandler(events.FileSystemEventHandler):
  """Subclass events.FileSystemEventHandler to respond to new files.
  """

  def __init__(self, callback):
    self._callback = callback
    super(CreatedFileHandler, self).__init__()

  def on_created(self, event):
    """Overrides super

    Args:
      event: events.FileCreated object representing created file
    """
    if not event.is_directory:
      self._callback(event.src_path)

class InvalidDirectory(Exception):

  def __init__(self, invalidDir):
    self._invalidDir = invalidDir

  def __repr__(self):
    return "InvalidDirectory: {0} is not a valid directory".format(
        self._invalidDir)

def watch(directory, callback, cmdQueue):
  """Watch the given directory and call `callback` on new files.

  Monitoring is done using the watchdog module, which will try to use the best
  asynchronous API available (kqueue on OS X/BSD, inotify on Linux,
  who-knows-what on Windows).

  Args:
    - directory: A string representing the path to the directory to watch.
    - callback: A function which will be called on each new file appearing in
      `directory`.
    - cmdQueue: a Queue.Queue for sending/receiving commands to/from the
      containing process.
  """
  if not os.path.isdir(directory):
    raise InvalidDirectory(directory)
  observer = observers.Observer()
  observer.schedule(CreatedFileHandler(callback), directory)
  observer.start()
  while True:
    cmd = cmdQueue.get()
    if cmd == config._STOP:
      observer.stop()
      observer.unschedule_all()
      observer.join()
      cmdQueue.task_done()
      break
    else:
      cmdQueue.put(cmd)
      time.sleep(1)

if __name__ == '__main__':
  import sys, Queue, threading
  if os.path.isdir(sys.argv[1]):
    def created(path):
      print "File added: {0}".format(path)
    cmdQ = Queue.Queue()
    t = threading.Thread(target=watch, args=[sys.argv[1], created, cmdQ])
    t.start()
    try:
      while True: time.sleep(1)
    except KeyboardInterrupt:
      cmdQ.put(config._STOP)
    cmdQ.join()
    t.join()
