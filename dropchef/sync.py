"""
Module for synchronizing & watching for updates.
"""
import time
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

def watch(directory, callback):
  """Watch the given directory and call `callback` on new files.

  Args:
    - directory: A string representing the path to the directory to watch
    - callback: A function which will be called on each new file appearing in
      `directory`
  """
  observer = observers.Observer()
  handler = CreatedFileHandler(callback)
  observer.schedule(handler, directory)
  observer.start()
  # TODO: Find a better way to do this - queue from controlling process?
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()

if __name__ == '__main__':
  import sys, os
  if os.path.isdir(sys.argv[1]):
    def created(path):
      print "File added: {0}".format(path)
    watch(sys.argv[1], created)
