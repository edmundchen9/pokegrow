#!/usr/bin/env python3
"""
Development runner for Discord bot
Automatically restarts bot when files change
"""

import subprocess
import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotRestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart_bot()
    
    def restart_bot(self):
        """Restart the bot process"""
        if self.process:
            print("🔄 Stopping bot...")
            self.process.terminate()
            self.process.wait()
        
        print("🚀 Starting bot...")
        self.process = subprocess.Popen([sys.executable, "main.py"])
    
    def on_modified(self, event):
        if event.src_path.endswith('.py') and not event.src_path.endswith('dev_run.py'):
            print(f"📝 File changed: {event.src_path}")
            print("🔄 Restarting bot...")
            time.sleep(1)  # Wait a moment for file to be fully written
            self.restart_bot()

def main():
    print("🛠️ Development Bot Runner")
    print("=" * 30)
    print("Watching for file changes...")
    print("Press Ctrl+C to stop")
    
    event_handler = BotRestartHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping development runner...")
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    
    observer.join()

if __name__ == "__main__":
    try:
        import watchdog
    except ImportError:
        print("❌ watchdog package not found!")
        print("Install it with: pip install watchdog")
        sys.exit(1)
    
    main()
