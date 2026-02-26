"""
Watcher Manager for AI Employee

This script manages multiple watchers and runs them concurrently.
"""
import logging
import threading
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure
    (vault_path / "Inbox").mkdir(exist_ok=True)
    (vault_path / "Needs_Action").mkdir(exist_ok=True)
    (vault_path / "Done").mkdir(exist_ok=True)

    # Import watchers
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    try:
        from watchers.gmail_watcher import GmailWatcher
        from watchers.whatsapp_watcher import WhatsAppWatcher
        from watchers.linkedin_watcher import LinkedInWatcher

        # Create instances of watchers
        gmail_watcher = GmailWatcher(str(vault_path))
        whatsapp_watcher = WhatsAppWatcher(str(vault_path))
        linkedin_watcher = LinkedInWatcher(str(vault_path))

        # Run watchers in separate threads
        threads = []

        # Create threads for each watcher
        gmail_thread = threading.Thread(target=gmail_watcher.run, daemon=True)
        whatsapp_thread = threading.Thread(target=whatsapp_watcher.run, daemon=True)
        linkedin_thread = threading.Thread(target=linkedin_watcher.run, daemon=True)

        threads = [gmail_thread, whatsapp_thread, linkedin_thread]

        # Start all threads
        for thread in threads:
            thread.start()
            logger.info(f"Started {thread.name}")

        logger.info("All watchers started. Press Ctrl+C to stop.")

        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping watchers...")

    except ImportError as e:
        logger.error(f"Error importing watchers: {e}")
        logger.info("Make sure all watcher files are properly created.")
    except Exception as e:
        logger.error(f"Error running watchers: {e}")

if __name__ == "__main__":
    main()