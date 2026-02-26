"""
Orchestrator for AI Employee

This script demonstrates Claude Code's ability to read from and write to the vault.
It simulates the basic flow of checking for items in Needs_Action, processing them,
and moving them to Done.
"""
import time
import logging
from pathlib import Path
from datetime import datetime
import json
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_needs_action_files(vault_path: Path):
    """Process all files in the Needs_Action folder"""
    needs_action_dir = vault_path / "Needs_Action"
    done_dir = vault_path / "Done"
    plans_dir = vault_path / "Plans"

    # Create Plans directory if it doesn't exist
    plans_dir.mkdir(exist_ok=True)

    # Only process files that start with "ACTION_" and are .md files (not the .original files)
    action_files = [f for f in needs_action_dir.glob("*.md") if f.name.startswith("ACTION_") and ".original." not in f.name]

    if not action_files:
        logger.info("No action files to process")
        return

    for action_file in action_files:
        logger.info(f"Processing action file: {action_file.name}")

        # Read the action file
        content = action_file.read_text()

        # Create a Plan.md file based on the action file content
        create_plan_file(action_file, content, plans_dir)

        # Update the content to mark as processed
        updated_content = content + f"\n\n## Processing Log\n- [x] Processed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n- [x] Plan created and moved to Done folder"

        # Update Dashboard.md with this activity
        dashboard_path = vault_path / "Dashboard.md"
        if dashboard_path.exists():
            dashboard_content = dashboard_path.read_text()
            activity_marker = "## Recent Activity"
            if activity_marker in dashboard_content:
                activity_section_start = dashboard_content.find(activity_marker)
                next_section_start = dashboard_content.find("\n## ", activity_section_start + len(activity_marker))
                if next_section_start == -1:  # If it's the last section
                    next_section_start = len(dashboard_content)

                current_activity = dashboard_content[activity_section_start:next_section_start]

                # Add new activity
                new_activity = f"- [x] {datetime.now().strftime('%Y-%m-%d %H:%M')} - Processed {action_file.name}"

                if new_activity not in current_activity:
                    updated_dashboard = (
                        dashboard_content[:activity_section_start + len(activity_marker)] +
                        f"\n{new_activity}" +
                        dashboard_content[activity_section_start + len(activity_marker):]
                    )
                    dashboard_path.write_text(updated_dashboard)
                    logger.info(f"Updated Dashboard.md with activity: {new_activity}")

        # Write the updated content back to the file
        action_file.write_text(updated_content)

        # Look for associated original file (with .original extension)
        original_extensions = ['.original.txt', '.original.md', '.original.pdf', '.original.doc', '.original.docx',
                              '.original.jpg', '.original.png', '.original.gif', '.original.csv', '.original.xlsx']
        original_file = None
        for ext in original_extensions:
            potential_file = action_file.with_suffix(ext)
            if potential_file.exists():
                original_file = potential_file
                break

        # Move the action file to Done folder
        done_file = done_dir / action_file.name
        action_file.rename(done_file)
        logger.info(f"Moved {action_file.name} to Done folder")

        # Move the original file to Done folder if it exists
        if original_file and original_file.exists():
            final_done_file = done_dir / original_file.name
            original_file.rename(final_done_file)
            logger.info(f"Moved original file {original_file.name} to Done folder")

        # Add a delay to simulate processing time
        time.sleep(0.5)

def create_plan_file(action_file: Path, content: str, plans_dir: Path):
    """Create a Plan.md file based on the action file content"""
    plan_filename = f"PLAN_{action_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    plan_path = plans_dir / plan_filename

    # Extract relevant information from action file to create a plan
    plan_content = f"""---
created: {datetime.now().isoformat()}
status: pending_approval
action_source: {action_file.name}
---

# Action Plan

## Objective
Process the request from the action file: {action_file.name}

## Context
{content[:500]}...  # First 500 characters of original content

## Tasks to Complete
- [ ] Review the original request
- [ ] Determine appropriate response/action
- [ ] Execute required actions
- [ ] Update status and move to done

## Approval Required
- [ ] Human review and approval of this plan

## Timeline
- Started: {datetime.now().isoformat()}
- Estimated completion: [TBD]
- Required by: [TBD]

## Success Criteria
- [ ] Request properly addressed
- [ ] Appropriate follow-up completed
- [ ] Status updated in system

## Notes
This plan was automatically generated by the AI Employee based on the action file {action_file.name}.
"""
    plan_path.write_text(plan_content)
    logger.info(f"Created plan file: {plan_path.name}")

    # Also create an approval request for sensitive actions
    create_approval_request(action_file, plans_dir)

def create_approval_request(action_file: Path, plans_dir: Path):
    """Create an approval request for sensitive actions"""
    # Check if this is a sensitive action that requires approval
    action_content = action_file.read_text()
    requires_approval = any(keyword in action_content.lower() for keyword in ['payment', 'invoice', 'money', 'payment', 'bank', 'financial'])

    if requires_approval:
        approval_filename = f"APPROVAL_{action_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        approval_path = plans_dir / "Pending_Approval" / approval_filename

        # Create Pending_Approval directory if it doesn't exist
        approval_path.parent.mkdir(exist_ok=True)

        approval_content = f"""---
type: approval_request
action_source: {action_file.name}
created: {datetime.now().isoformat()}
status: pending
---

# Approval Required

## Action Details
- **Source File:** {action_file.name}
- **Request Type:** Sensitive action requiring approval
- **Created:** {datetime.now().isoformat()}

## To Approve
1. Review the original action file
2. Verify the planned response is appropriate
3. Move this file to the /Approved folder

## To Reject
Move this file to the /Rejected folder with reasons.

## Action Summary
This action requires human approval before proceeding. Please review the source file and determine if the planned action is appropriate.
"""
        approval_path.write_text(approval_content)
        logger.info(f"Created approval request: {approval_path.name}")

def main():
    vault_path = Path("../AI_Employee_Vault")

    logger.info(f"Starting orchestrator for vault: {vault_path}")

    # Create necessary directories
    (vault_path / "Needs_Action").mkdir(exist_ok=True)
    (vault_path / "Done").mkdir(exist_ok=True)
    (vault_path / "Inbox").mkdir(exist_ok=True)
    (vault_path / "Plans").mkdir(exist_ok=True)
    (vault_path / "Plans" / "Pending_Approval").mkdir(exist_ok=True)
    (vault_path / "Plans" / "Approved").mkdir(exist_ok=True)
    (vault_path / "Plans" / "Rejected").mkdir(exist_ok=True)

    # Initialize Dashboard if it doesn't exist
    dashboard_path = vault_path / "Dashboard.md"
    if not dashboard_path.exists():
        dashboard_content = f"""# AI Employee Dashboard

## Executive Summary
This dashboard provides an overview of your AI Employee's activities and status.

## Recent Activity
- [ ] System initialization in progress

## Pending Tasks
- [ ] Set up company handbook
- [ ] Configure watchers
- [ ] Test file system monitoring

## System Status
- Watchers: Active
- MCP Servers: Not configured
- Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Quick Stats
- Files Processed: 0
- Actions Taken: 0
- Approval Requests: 0
"""
        dashboard_path.write_text(dashboard_content)

    # Process any existing action files
    process_needs_action_files(vault_path)

    # Process any approval requests
    process_approval_requests(vault_path)

    # Update system status in dashboard
    if dashboard_path.exists():
        dashboard_content = dashboard_path.read_text()
        status_marker = "## System Status"
        if status_marker in dashboard_content:
            # Find the "Last Update:" part and replace the entire line
            import re
            updated_dashboard = re.sub(
                r'Last Update:.*$',
                f'Last Update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                dashboard_content,
                flags=re.MULTILINE
            )
            # Also update the watchers status if needed
            if "- Watchers: Inactive" in updated_dashboard:
                updated_dashboard = updated_dashboard.replace(
                    "- Watchers: Inactive",
                    "- Watchers: Active"
                )
            dashboard_path.write_text(updated_dashboard)

    logger.info("Orchestrator completed one cycle")

def process_approval_requests(vault_path: Path):
    """Process approval request files in the Pending_Approval folder"""
    pending_approval_dir = vault_path / "Plans" / "Pending_Approval"
    approved_dir = vault_path / "Plans" / "Approved"
    rejected_dir = vault_path / "Plans" / "Rejected"

    # Create directories if they don't exist
    approved_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)

    approval_files = list(pending_approval_dir.glob("*.md"))

    if not approval_files:
        logger.info("No approval requests to process")
        return

    for approval_file in approval_files:
        logger.info(f"Processing approval request: {approval_file.name}")
        # In a real implementation, this would check if the file has been moved
        # by a human to either Approved or Rejected folder
        # For now, we'll just log that an approval request exists

if __name__ == "__main__":
    main()