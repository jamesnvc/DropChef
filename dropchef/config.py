import os

_STOP = 'stop'

templateDir = ''
postTemplate = os.path.join(
    os.path.expanduser(templateDir),
    '_config', 'post.html')
dropboxDir = os.path.expanduser('~/Dropbox')
postsDirectory = os.path.join(
    os.path.expanduser(dropboxDir),
    'apps', 'dropChef', 'posts')
queueDir = os.path.join(
    postsDirectory, 'queue')
publishedDir = os.path.join(
    postsDirectory, 'published')
