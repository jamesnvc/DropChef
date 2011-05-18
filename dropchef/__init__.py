from . import bake
from . import config
from . import sync
import os
import Queue

def runMain(appDirectory):
    """Start the dropchef watching the directory, baking when it's time."""

    def newPostHandler(newPost):
        bakedContent = bake.bake(newPost)
        bakedPostFile = os.path.join(
            config.publishedDir, os.path.basename(newPost))
        with open(bakedPostFile, 'w') as f:
            f.write(bakedContent)
        os.unlink(newPost)
        # TODO: Regen/update site
    cmdQ = Queue.Queue()
    sync.watch(config.queueDir, newPostHandler, cmdQ)
