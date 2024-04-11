import logging
import os
import threading
import time
from typing import Callable

logger = logging.getLogger(__name__)


class HotReload:
    """
    Monitors the given directory for changes and calls the callback on change.
    """

    def __init__(self, directory: str = ".", callback: Callable = lambda: None) -> None:
        self.directory = directory
        self.callback = callback
        self.file_mtimes = {}

    def start(self) -> None:
        """Starts the monitoring in a separate thread."""

        t = threading.Thread(target=self._monitor_files)
        t.daemon = True
        t.start()

    def _monitor_files(self) -> None:
        """Monitors the directory for changes and calls the callback on change."""

        while True:
            changed = self._check_files()
            if changed:
                self.callback()
                break
            time.sleep(1)

    def _check_files(self) -> bool:
        """
        Check for any file changes in the directory.

        Returns:
            True if a change was detected, False otherwise.
        """
        has_changed = False
        for root, _, files in os.walk(self.directory):
            for filename in files:
                if not filename.endswith(".py"):
                    continue
                filepath = os.path.join(root, filename)
                mtime = os.path.getmtime(filepath)
                if filepath not in self.file_mtimes:
                    self.file_mtimes[filepath] = mtime
                elif self.file_mtimes[filepath] != mtime:
                    print(f"Change detected in {filepath}. Restarting...")
                    self.file_mtimes[filepath] = mtime
                    has_changed = True
        return has_changed
