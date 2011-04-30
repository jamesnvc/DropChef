"""
Module for synchronizing & watching for updates.
"""
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
  """Watch the given directory  and call `callback` on new files.

  Args:
    - directory: A string representing the path to the directory to watch
    - callback: A function which will be called on each new file appearing in
      `directory`
  """
  observer = observers.Observers
  handler = CreatedFileHandler(callback)
  observers.schedule(handler, directory)

