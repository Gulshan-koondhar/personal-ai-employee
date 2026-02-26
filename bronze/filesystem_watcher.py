"""
File System Watcher for AI Employee

This script monitors a designated drop folder and creates action files
when new files are detected, moving them to the /Needs_Action folder.
"""
import time
import logging
from pathlib import Path
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events in the drop folder"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.drop_folder = self.vault_path / 'Inbox'

        # Create directories if they don't exist
        self.needs_action.mkdir(exist_ok=True)
        self.drop_folder.mkdir(exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)

        # Skip temporary files that may be in the process of being written
        if source.suffix.startswith('.tmp') or source.name.startswith('~'):
            return

        # Check if file exists and is accessible
        if not source.exists():
            logger.warning(f"File no longer exists: {source.name}")
            return

        logger.info(f"New file detected: {source.name}")

        # Create an action file in Needs_Action folder
        self.create_action_file(source)

    def on_moved(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        logger.info(f"File moved to drop folder: {source.name}")
        self.create_action_file(source)

    def create_action_file(self, source: Path):
        """Create an action file in Needs_Action folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        action_filename = f"ACTION_{timestamp}_{source.name}.md"
        action_path = self.needs_action / action_filename

        # Create metadata with file information
        file_size = source.stat().st_size
        file_ext = source.suffix.lower()

        # Determine action type based on file extension
        if file_ext in ['.pdf', '.doc', '.docx']:
            action_type = "document_review"
            priority = "medium"
        elif file_ext in ['.jpg', '.png', '.gif']:
            action_type = "image_review"
            priority = "low"
        elif file_ext in ['.csv', '.xlsx']:
            action_type = "data_analysis"
            priority = "high"
        else:
            action_type = "general_file"
            priority = "medium"

        content = f"""---
type: file_drop
original_name: {source.name}
size: {file_size} bytes
extension: {file_ext}
priority: {priority}
status: pending
created: {datetime.now().isoformat()}
---

# File Processing Request

## File Information
- **Original Name:** {source.name}
- **Size:** {file_size} bytes
- **Type:** {file_ext}
- **Detected Action:** {action_type}

## Processing Status
- [ ] File reviewed
- [ ] Action determined
- [ ] Processed
- [ ] Moved to Done

## Suggested Actions
- [ ] Review content
- [ ] Determine next steps
- [ ] Update Dashboard.md

## Notes
New file dropped in the Inbox folder for processing.
"""
        action_path.write_text(content)
        logger.info(f"Created action file: {action_path.name}")

        # Move the original file to the action file's directory so it's available during processing
        # This preserves the original file but removes it from the Inbox
        original_copy = action_path.with_suffix('.original' + source.suffix)
        shutil.move(str(source), str(original_copy))  # Move instead of copy
        logger.info(f"Moved original file to: {original_copy.name}")

def main():
    vault_path = Path("../AI_Employee_Vault")

    # Create the vault structure if it doesn't exist
    (vault_path / "Inbox").mkdir(exist_ok=True)
    (vault_path / "Needs_Action").mkdir(exist_ok=True)
    (vault_path / "Done").mkdir(exist_ok=True)

    event_handler = DropFolderHandler(str(vault_path))
    observer = Observer()
    observer.schedule(event_handler, str(vault_path / "Inbox"), recursive=False)

    logger.info(f"Starting file system watcher for {vault_path}/Inbox")
    logger.info("Press Ctrl+C to stop the watcher")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watcher stopped by user")
    observer.join()

if __name__ == "__main__":
    main()