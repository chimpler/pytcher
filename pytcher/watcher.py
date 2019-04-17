import logging

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logger = logging.getLogger(__name__)


class Watcher(FileSystemEventHandler):

    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        logger.info('File change detected. Restarting app...')
        self.app.restart()

    def start(self):
        observer = Observer()
        observer.schedule(self, path='.', recursive=False)
        observer.start()
