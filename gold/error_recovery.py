"""
Error Recovery and Graceful Degradation for AI Employee

This module handles error recovery and graceful degradation for the Gold Tier.
"""
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
import json
import sys
import os
import traceback
from typing import Dict, Any, Callable, Optional
from contextlib import contextmanager

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ErrorRecoveryManager:
    """Manages error recovery and graceful degradation for the AI Employee"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.logs_dir = self.vault_path / "Logs"
        self.backup_dir = self.vault_path / "Backups"
        self.failed_actions_dir = self.vault_path / "Failed_Actions"

        # Create necessary directories
        self.logs_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.failed_actions_dir.mkdir(exist_ok=True)

        # Error tracking
        self.error_log_file = self.logs_dir / f"error_log_{datetime.now().strftime('%Y%m%d')}.jsonl"
        self.recovery_attempts = {}
        self.max_recovery_attempts = 3

    def log_error(self, error: Exception, context: str = "", severity: str = "medium") -> str:
        """
        Log an error with context and severity level.

        Args:
            error: The exception that occurred
            context: Context where the error occurred
            severity: Severity level ('low', 'medium', 'high', 'critical')

        Returns:
            Error ID for tracking
        """
        error_id = f"error_{int(time.time() * 1000000)}"
        error_info = {
            "error_id": error_id,
            "timestamp": datetime.now().isoformat(),
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "severity": severity,
            "traceback": traceback.format_exc(),
            "session_id": os.environ.get("SESSION_ID", "local_session")
        }

        # Write to error log file
        with open(self.error_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_info) + '\n')

        logger.error(f"Error {error_id} ({severity}): {context} - {str(error)}")

        return error_id

    def graceful_degrade(self, operation: Callable, fallback: Callable, context: str = "") -> Any:
        """
        Execute an operation with graceful degradation fallback.

        Args:
            operation: Primary operation to attempt
            fallback: Fallback operation if primary fails
            context: Context for logging

        Returns:
            Result of primary operation or fallback
        """
        try:
            result = operation()
            logger.info(f"Operation succeeded: {context}")
            return result
        except Exception as e:
            error_id = self.log_error(e, f"{context} (primary operation failed)", "medium")
            logger.warning(f"Falling back after error {error_id}: {context}")

            try:
                result = fallback()
                logger.info(f"Fallback succeeded: {context}")
                return result
            except Exception as fallback_error:
                fallback_error_id = self.log_error(fallback_error, f"{context} (fallback failed)", "high")
                logger.error(f"Both primary and fallback failed ({error_id}, {fallback_error_id}): {context}")
                raise fallback_error

    def retry_with_backoff(self, operation: Callable, max_attempts: int = 3,
                          backoff_base: float = 1.0, context: str = "") -> Any:
        """
        Retry an operation with exponential backoff.

        Args:
            operation: Operation to retry
            max_attempts: Maximum number of retry attempts
            backoff_base: Base delay between attempts (seconds)
            context: Context for logging

        Returns:
            Result of successful operation
        """
        for attempt in range(1, max_attempts + 1):
            try:
                result = operation()
                logger.info(f"Operation succeeded on attempt {attempt}/{max_attempts}: {context}")
                return result
            except Exception as e:
                if attempt < max_attempts:
                    delay = backoff_base * (2 ** (attempt - 1))  # Exponential backoff
                    error_id = self.log_error(e, f"{context} (attempt {attempt}/{max_attempts})", "medium")
                    logger.warning(f"Attempt {attempt} failed ({error_id}). Retrying in {delay}s: {context}")
                    time.sleep(delay)
                else:
                    error_id = self.log_error(e, f"{context} (all {max_attempts} attempts failed)", "high")
                    logger.error(f"All {max_attempts} attempts failed ({error_id}): {context}")
                    raise e

    def backup_file(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of a file.

        Args:
            file_path: Path to the file to backup

        Returns:
            Path to the backup file, or None if backup failed
        """
        if not file_path.exists():
            logger.warning(f"Cannot backup non-existent file: {file_path}")
            return None

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_filename

            # Read the file content
            content = file_path.read_text(encoding='utf-8')

            # Write to backup
            backup_path.write_text(content, encoding='utf-8')

            logger.info(f"Backup created: {file_path.name} -> {backup_path.name}")
            return backup_path
        except Exception as e:
            error_id = self.log_error(e, f"Backup failed for {file_path}", "high")
            logger.error(f"Backup failed ({error_id}): {file_path}")
            return None

    def restore_from_backup(self, file_path: Path, backup_path: Path) -> bool:
        """
        Restore a file from backup.

        Args:
            file_path: Path to the file to restore
            backup_path: Path to the backup file

        Returns:
            True if restore was successful, False otherwise
        """
        try:
            if not backup_path.exists():
                logger.error(f"Backup file does not exist: {backup_path}")
                return False

            # Read from backup
            content = backup_path.read_text(encoding='utf-8')

            # Write to target file
            file_path.write_text(content, encoding='utf-8')

            logger.info(f"Restored from backup: {backup_path.name} -> {file_path.name}")
            return True
        except Exception as e:
            error_id = self.log_error(e, f"Restore failed for {file_path} from {backup_path}", "critical")
            logger.error(f"Restore failed ({error_id}): {file_path} from {backup_path}")
            return False

    def save_failed_action(self, action_data: Dict[str, Any], error_info: Dict[str, Any]) -> Path:
        """
        Save a failed action for later processing.

        Args:
            action_data: Original action data that failed
            error_info: Error information

        Returns:
            Path to the saved failed action file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        action_id = action_data.get('id', action_data.get('action_id', 'unknown'))
        failed_filename = f"FAILED_{action_id}_{timestamp}.json"
        failed_path = self.failed_actions_dir / failed_filename

        failed_action_data = {
            "original_action": action_data,
            "error_info": error_info,
            "failed_at": datetime.now().isoformat(),
            "retry_count": 0,
            "status": "failed"
        }

        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump(failed_action_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved failed action: {failed_filename}")
        return failed_path

    def process_failed_actions(self) -> Dict[str, int]:
        """
        Process previously failed actions with recovery attempts.

        Returns:
            Dictionary with processing results
        """
        failed_files = list(self.failed_actions_dir.glob("FAILED_*.json"))

        results = {
            "attempted": 0,
            "recovered": 0,
            "permanently_failed": 0
        }

        for failed_file in failed_files:
            try:
                with open(failed_file, 'r', encoding='utf-8') as f:
                    failed_data = json.load(f)

                if failed_data['retry_count'] >= self.max_recovery_attempts:
                    logger.info(f"Max retries reached for {failed_file.name}, moving to permanently failed")
                    # Move to a separate directory or mark as permanently failed
                    results["permanently_failed"] += 1
                    continue

                results["attempted"] += 1
                logger.info(f"Attempting recovery for {failed_file.name}")

                # Try to re-execute the action with retry logic
                def retry_operation():
                    # In this demo, we'll just mark as recovered - in real system,
                    # this would re-execute the original action
                    return True

                try:
                    self.retry_with_backoff(
                        retry_operation,
                        max_attempts=2,
                        context=f"Recovery for {failed_file.name}"
                    )

                    # If successful, remove the failed action file
                    failed_file.unlink()
                    results["recovered"] += 1
                    logger.info(f"Successfully recovered {failed_file.name}")
                except Exception:
                    # Update retry count
                    failed_data["retry_count"] += 1
                    failed_data["last_retry"] = datetime.now().isoformat()
                    failed_data["status"] = "retry_failed"

                    with open(failed_file, 'w') as f:
                        json.dump(failed_data, f, indent=2, ensure_ascii=False)

            except Exception as e:
                error_id = self.log_error(e, f"Processing failed action {failed_file.name}", "high")
                logger.error(f"Error processing failed action ({error_id}): {failed_file.name}")

        return results

    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the system.

        Returns:
            Health check results
        """
        now = datetime.now()

        # Check various system components
        checks = {
            "timestamp": now.isoformat(),
            "vault_accessible": self.vault_path.exists(),
            "logs_writable": self.logs_dir.exists(),
            "backup_space_available": self._check_disk_space(self.backup_dir),
            "failed_actions_count": len(list(self.failed_actions_dir.glob("FAILED_*.json"))),
            "recent_errors_count": self._count_recent_errors(hours=24),
            "system_uptime": self._get_system_uptime()
        }

        # Overall health status
        issues = []
        if checks["failed_actions_count"] > 10:
            issues.append("High number of failed actions")
        if checks["recent_errors_count"] > 5:
            issues.append("High number of recent errors")
        if not checks["vault_accessible"]:
            issues.append("Vault not accessible")
        if checks["backup_space_available"] < 100:  # Less than 100MB
            issues.append("Low backup disk space")

        checks["overall_status"] = "degraded" if issues else "healthy"
        checks["issues"] = issues

        return checks

    def _check_disk_space(self, path: Path) -> float:
        """Check available disk space in MB."""
        try:
            import shutil
            total, used, free = shutil.disk_usage(path)
            return free / (1024 * 1024)  # Convert to MB
        except:
            return 0

    def _count_recent_errors(self, hours: int = 24) -> int:
        """Count errors in the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        count = 0

        try:
            with open(self.error_log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            error_data = json.loads(line)
                            error_time = datetime.fromisoformat(error_data['timestamp'].replace('Z', '+00:00'))
                            if error_time >= cutoff_time:
                                count += 1
                        except:
                            continue
        except FileNotFoundError:
            pass  # No error log yet

        return count

    def _get_system_uptime(self) -> str:
        """Get system uptime (simulated)."""
        # In a real implementation, this would track the actual system start time
        return "24h 5m 30s"  # Simulated uptime

@contextmanager
def error_handling_context(recovery_manager: ErrorRecoveryManager, context: str = ""):
    """
    Context manager for handling errors gracefully.

    Args:
        recovery_manager: ErrorRecoveryManager instance
        context: Context for logging
    """
    try:
        yield
    except Exception as e:
        error_id = recovery_manager.log_error(e, f"Context: {context}", "medium")
        logger.error(f"Error in context '{context}' ({error_id}): {str(e)}")
        raise  # Re-raise the exception after logging

def main():
    """Main function to demonstrate error recovery and graceful degradation"""
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure if needed
    (vault_path / "Needs_Action").mkdir(exist_ok=True)

    recovery_manager = ErrorRecoveryManager(str(vault_path))

    print("Testing graceful degradation...")

    # Test 1: Graceful degradation
    def primary_operation():
        raise Exception("Primary operation failed intentionally")

    def fallback_operation():
        return "Fallback result"

    try:
        result = recovery_manager.graceful_degrade(
            primary_operation,
            fallback_operation,
            "Test graceful degradation"
        )
        print(f"Graceful degradation result: {result}")
    except Exception as e:
        print(f"Graceful degradation failed: {e}")

    # Test 2: Retry with backoff
    print("\nTesting retry with backoff...")

    attempt_count = 0
    def operation_with_eventual_success():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise Exception(f"Still failing on attempt {attempt_count}")
        return f"Success on attempt {attempt_count}"

    try:
        attempt_count = 0
        result = recovery_manager.retry_with_backoff(
            operation_with_eventual_success,
            max_attempts=5,
            context="Test retry with backoff"
        )
        print(f"Retry with backoff result: {result}")
    except Exception as e:
        print(f"Retry with backoff failed: {e}")

    # Test 3: Backup and restore
    print("\nTesting backup functionality...")

    # Create a test file
    test_file = vault_path / "Needs_Action" / "test_file_for_backup.md"
    test_file.write_text("This is a test file that might need backup functionality.")

    # Create backup
    backup_path = recovery_manager.backup_file(test_file)
    if backup_path:
        print(f"Backup created: {backup_path.name}")

        # Modify original file
        test_file.write_text("This file has been modified after backup.")

        # Restore from backup
        success = recovery_manager.restore_from_backup(test_file, backup_path)
        print(f"Restore result: {success}")

    # Test 4: Health check
    print("\nRunning health check...")
    health_results = recovery_manager.health_check()
    print(f"Health check results: {health_results}")

    # Test 5: Error context manager
    print("\nTesting error context manager...")
    try:
        with error_handling_context(recovery_manager, "test context"):
            raise ValueError("Test error in context manager")
    except ValueError:
        print("Context manager caught and logged the error")

    print("\nError recovery and graceful degradation demo completed!")

if __name__ == "__main__":
    main()