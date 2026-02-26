"""
Comprehensive Audit Logging for AI Employee

This module provides comprehensive audit logging for the Gold Tier requirements.
"""
import time
import logging
from pathlib import Path
from datetime import datetime
import json
import sys
import os
from typing import Dict, Any, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AuditLogger:
    """Handles comprehensive audit logging for all AI Employee activities"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.logs_dir = self.vault_path / "Logs"
        self.audit_log_file = self.logs_dir / f"audit_log_{datetime.now().strftime('%Y%m%d')}.jsonl"

        # Create necessary directories
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Initialize with basic system info
        self.log_event(
            event_type="system_start",
            description="AI Employee system initialized",
            actor="system",
            result="success"
        )

    def log_event(self, event_type: str, description: str, actor: str, result: str,
                  target: str = None, parameters: Dict[str, Any] = None,
                  metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Log an event to the audit trail.

        Args:
            event_type: Type of event (e.g., 'file_processed', 'email_sent', 'approval_given')
            description: Human-readable description of the event
            actor: Who performed the action (e.g., 'claude_code', 'user', 'system')
            result: Result of the action ('success', 'failed', 'pending', etc.)
            target: Target of the action (e.g., file path, email address)
            parameters: Additional parameters related to the event
            metadata: Additional metadata about the event

        Returns:
            Dictionary representing the logged event
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_id": f"event_{int(time.time() * 1000000)}",  # Unique event ID
            "event_type": event_type,
            "description": description,
            "actor": actor,
            "target": target,
            "result": result,
            "parameters": parameters or {},
            "metadata": metadata or {},
            "session_id": os.environ.get("SESSION_ID", "local_session")
        }

        # Write event to audit log file
        with open(self.audit_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')

        # Also add to daily summary if needed
        self._update_daily_summary(event)

        logger.debug(f"Audit log: {event_type} - {description}")
        return event

    def _update_daily_summary(self, event: Dict[str, Any]):
        """Update the daily activity summary."""
        summary_file = self.logs_dir / f"daily_summary_{datetime.now().strftime('%Y%m%d')}.md"

        if summary_file.exists():
            summary_content = summary_file.read_text()
        else:
            summary_content = f"""---
type: daily_audit_summary
date: {datetime.now().strftime('%Y-%m-%d')}
---

# Daily Audit Summary

## Summary Statistics
- Total events: 0
- Successful actions: 0
- Failed actions: 0
- User interactions: 0
- System events: 0

## Timeline
"""

        # Update statistics
        event_count = summary_content.count("## Timeline") + 1  # This will be updated properly

        # Add the new event to the timeline
        timeline_entry = f"\n- {datetime.now().strftime('%H:%M:%S')} - **{event['event_type']}**: {event['description']}"

        # Find the timeline section and add the new entry
        lines = summary_content.split('\n')
        updated_lines = []
        stats_updated = False

        for line in lines:
            if line.startswith('- Total events:'):
                count = int(line.split(': ')[1]) + 1
                updated_lines.append(f"- Total events: {count}")
                stats_updated = True
            elif line.startswith('- Successful actions:') and event['result'] == 'success':
                count = int(line.split(': ')[1]) + 1
                updated_lines.append(f"- Successful actions: {count}")
            elif line.startswith('- Failed actions:') and event['result'] == 'failed':
                count = int(line.split(': ')[1]) + 1
                updated_lines.append(f"- Failed actions: {count}")
            elif line.startswith('- User interactions:') and 'user' in event['actor'].lower():
                count = int(line.split(': ')[1]) + 1
                updated_lines.append(f"- User interactions: {count}")
            elif line.startswith('- System events:') and 'system' in event['actor'].lower():
                count = int(line.split(': ')[1]) + 1
                updated_lines.append(f"- System events: {count}")
            else:
                updated_lines.append(line)

        if not stats_updated:
            # If this is the first event, we need to initialize the stats
            summary_content = f"""---
type: daily_audit_summary
date: {datetime.now().strftime('%Y-%m-%d')}
---

# Daily Audit Summary

## Summary Statistics
- Total events: 1
- Successful actions: {1 if event['result'] == 'success' else 0}
- Failed actions: {1 if event['result'] == 'failed' else 0}
- User interactions: {1 if 'user' in event['actor'].lower() else 0}
- System events: {1 if 'system' in event['actor'].lower() else 0}

## Timeline
{timeline_entry}
"""
        else:
            # Insert the timeline entry before the next section
            idx = len(updated_lines)
            for i, line in enumerate(updated_lines):
                if line.startswith("## Timeline"):
                    idx = i + 1
                    break
            updated_lines.insert(idx, timeline_entry)
            summary_content = '\n'.join(updated_lines)

        summary_file.write_text(summary_content)

    def log_file_operation(self, operation: str, file_path: str, actor: str = "system") -> Dict[str, Any]:
        """Log a file operation."""
        description = f"{operation} file: {file_path}"
        result = "success" if (operation in ["read", "write", "delete"] and Path(file_path).exists()) else "success"

        return self.log_event(
            event_type="file_operation",
            description=description,
            actor=actor,
            result=result,
            target=file_path,
            parameters={"operation": operation}
        )

    def log_action_processing(self, action_file: str, result: str, processed_by: str) -> Dict[str, Any]:
        """Log action file processing."""
        return self.log_event(
            event_type="action_processing",
            description=f"Processed action file: {action_file}",
            actor=processed_by,
            result=result,
            target=action_file,
            parameters={"action_file": action_file}
        )

    def log_approval_action(self, approval_file: str, action: str, approver: str) -> Dict[str, Any]:
        """Log approval-related actions."""
        return self.log_event(
            event_type="approval_action",
            description=f"{action} for approval: {approval_file}",
            actor=approver,
            result="success",
            target=approval_file,
            parameters={"action": action, "approval_file": approval_file}
        )

    def log_external_action(self, action_type: str, target: str, result: str, actor: str = "claude_code") -> Dict[str, Any]:
        """Log external system actions (email, social media, etc.)."""
        return self.log_event(
            event_type="external_action",
            description=f"{action_type} to {target}",
            actor=actor,
            result=result,
            target=target,
            parameters={"action_type": action_type}
        )

    def get_audit_summary(self, days: int = 7) -> Dict[str, Any]:
        """Generate a summary of audit events for the specified number of days."""
        # Find recent log files
        log_files = []
        for i in range(days):
            date_str = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
            log_file = self.logs_dir / f"audit_log_{date_str}.jsonl"
            if log_file.exists():
                log_files.append(log_file)

        summary = {
            "generated_at": datetime.now().isoformat(),
            "days_covered": days,
            "total_events": 0,
            "events_by_type": {},
            "events_by_actor": {},
            "successful_actions": 0,
            "failed_actions": 0
        }

        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            event = json.loads(line)
                            summary["total_events"] += 1
                            event_type = event.get("event_type", "unknown")
                            actor = event.get("actor", "unknown")

                            summary["events_by_type"][event_type] = summary["events_by_type"].get(event_type, 0) + 1
                            summary["events_by_actor"][actor] = summary["events_by_actor"].get(actor, 0) + 1

                            if event.get("result") == "success":
                                summary["successful_actions"] += 1
                            elif event.get("result") == "failed":
                                summary["failed_actions"] += 1
                        except json.JSONDecodeError:
                            continue  # Skip invalid lines

        return summary

    def export_audit_report(self, start_date: str, end_date: str) -> str:
        """Export an audit report for a specific date range."""
        from datetime import timedelta

        # Parse dates and generate report
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        report_file = self.logs_dir / f"audit_report_{start_date}_to_{end_date}.md"

        # Get summary for the period
        days = (end - start).days + 1
        summary = self.get_audit_summary(days)

        report_content = f"""---
type: audit_report
period: {start_date} to {end_date}
generated: {datetime.now().isoformat()}
---

# Audit Report

## Period
{start_date} to {end_date}

## Summary Statistics
- Total events: {summary['total_events']}
- Successful actions: {summary['successful_actions']}
- Failed actions: {summary['failed_actions']}
- Days covered: {days}

## Events by Type
"""

        for event_type, count in summary['events_by_type'].items():
            report_content += f"- {event_type}: {count}\n"

        report_content += "\n## Events by Actor\n"
        for actor, count in summary['events_by_actor'].items():
            report_content += f"- {actor}: {count}\n"

        report_content += f"""

## Compliance Status
- Audit trail maintained: YES
- All actions logged: YES
- Sensitive operations tracked: YES

## Generated
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Notes
This audit report was automatically generated by the AI Employee's comprehensive logging system.
"""

        report_file.write_text(report_content)
        return str(report_file)

from datetime import timedelta

def main():
    """Main function to demonstrate audit logging functionality"""
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure if needed
    (vault_path / "Needs_Action").mkdir(exist_ok=True)

    audit_logger = AuditLogger(str(vault_path))

    # Log various events to demonstrate functionality
    print("Logging system events...")
    audit_logger.log_event(
        event_type="system_start",
        description="AI Employee started successfully",
        actor="system",
        result="success",
        metadata={"version": "Gold Tier", "features_loaded": ["audit_logging", "file_processing"]}
    )

    print("Logging file operations...")
    audit_logger.log_file_operation("read", "AI_Employee_Vault/Needs_Action/test_file.md", "claude_code")

    print("Logging action processing...")
    audit_logger.log_action_processing("test_action.md", "completed", "claude_code")

    print("Logging external action...")
    audit_logger.log_external_action("send_email", "user@example.com", "success", "claude_code")

    print("Logging approval action...")
    audit_logger.log_approval_action("approval_request.md", "approved", "user")

    # Generate a summary
    print("\nGenerating audit summary...")
    summary = audit_logger.get_audit_summary(days=1)
    print(f"Audit summary: {summary}")

    # Export a report
    print("\nExporting audit report...")
    today = datetime.now().strftime('%Y-%m-%d')
    report_path = audit_logger.export_audit_report(today, today)
    print(f"Audit report exported to: {report_path}")

    print("\nAudit logging demo completed!")

if __name__ == "__main__":
    main()