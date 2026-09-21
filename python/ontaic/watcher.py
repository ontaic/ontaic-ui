"""File watcher for hot-reload support."""
import time
import os
from pathlib import Path
from typing import Callable, List, Optional
import threading


class FileWatcher:
    """Watches files for changes and triggers callbacks."""

    def __init__(
        self,
        paths: List[str],
        callback: Callable,
        debounce_ms: int = 300,
        extensions: Optional[List[str]] = None,
    ):
        self.paths = [Path(p) for p in paths]
        self.callback = callback
        self.debounce_ms = debounce_ms
        self.extensions = extensions or [".py"]
        self._last_run = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._file_times: dict = {}

    def start(self):
        """Start watching files."""
        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        print(f"[ontaic-watcher] Watching {len(self.paths)} paths for changes")

    def stop(self):
        """Stop watching files."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _watch_loop(self):
        """Main watch loop."""
        # Initial scan
        self._scan_files()

        while self._running:
            time.sleep(0.5)  # Check every 500ms

            if self._has_changes():
                now = time.time() * 1000
                if now - self._last_run > self.debounce_ms:
                    self._last_run = now
                    print("[ontaic-watcher] Changes detected, recompiling...")
                    try:
                        self.callback()
                    except Exception as e:
                        print(f"[ontaic-watcher] Error: {e}")

    def _scan_files(self):
        """Scan all files and record modification times."""
        self._file_times = {}
        for path in self.paths:
            if path.is_file():
                self._file_times[str(path)] = path.stat().st_mtime
            elif path.is_dir():
                for ext in self.extensions:
                    for file in path.rglob(f"*{ext}"):
                        if "__pycache__" not in str(file):
                            self._file_times[str(file)] = file.stat().st_mtime

    def _has_changes(self) -> bool:
        """Check if any files have changed."""
        current_times = {}

        for path in self.paths:
            if path.is_file():
                try:
                    current_times[str(path)] = path.stat().st_mtime
                except OSError:
                    pass
            elif path.is_dir():
                for ext in self.extensions:
                    for file in path.rglob(f"*{ext}"):
                        if "__pycache__" not in str(file):
                            try:
                                current_times[str(file)] = file.stat().st_mtime
                            except OSError:
                                pass

        # Check for new or modified files
        for file_path, mtime in current_times.items():
            if file_path not in self._file_times or self._file_times[file_path] != mtime:
                self._file_times = current_times
                return True

        # Check for deleted files
        if len(current_times) != len(self._file_times):
            self._file_times = current_times
            return True

        return False
