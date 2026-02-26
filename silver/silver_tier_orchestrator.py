"""
Silver Tier Orchestrator for AI Employee

This orchestrator manages the integration between different silver tier
components (Gmail, WhatsApp, LinkedIn watchers) and provides unified
workflow management similar to the bronze tier but with silver tier
capabilities like social media integration, scheduling, and human-in-the-loop
approval workflows.
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
    """Process all files in the Needs_Action folder, prioritizing social media related actions"""
    needs_action_dir = vault_path / "Needs_Action"
    done_dir = vault_path / "Done"
    plans_dir = vault_path / "Plans"
    linkedin_posts_dir = vault_path / "LinkedIn_Posts"
    social_posts_dir = vault_path / "Social_Posts"

    # Create directories if they don't exist
    plans_dir.mkdir(exist_ok=True)
    linkedin_posts_dir.mkdir(exist_ok=True)
    social_posts_dir.mkdir(exist_ok=True)

    # Only process files that start with "ACTION_" and are .md files (not the .original files)
    action_files = [f for f in needs_action_dir.glob("*.md") if (f.name.startswith("ACTION_") or f.name.startswith("EMAIL_") or "social" in f.name.lower()) and ".original." not in f.name]

    if not action_files:
        logger.info("No action files to process in silver tier")
        return

    for action_file in action_files:
        logger.info(f"Processing action file in silver tier: {action_file.name}")

        # Read the action file
        content = action_file.read_text()

        # Check if this is a social media related action
        is_social_action = any(keyword in content.lower() for keyword in
                              ['linkedin', 'social', 'post', 'tweet', 'facebook', 'instagram'])

        # Create a Plan.md file based on the action file content
        create_silver_plan_file(action_file, content, plans_dir, is_social_action)

        # Update the content to mark as processed
        updated_content = content + f"\n\n## Silver Tier Processing Log\n- [x] Processed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n- [x] Silver plan created and managed"

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
                new_activity = f"- [x] {datetime.now().strftime('%Y-%m-%d %H:%M')} - Silver Tier processed {action_file.name}"

                if new_activity not in current_activity:
                    updated_dashboard = (
                        dashboard_content[:activity_section_start + len(activity_marker)] +
                        f"\n{new_activity}" +
                        dashboard_content[activity_section_start + len(activity_marker):]
                    )
                    dashboard_path.write_text(updated_dashboard)
                    logger.info(f"Updated Dashboard.md with silver tier activity: {new_activity}")

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

def create_silver_plan_file(action_file: Path, content: str, plans_dir: Path, is_social_action: bool):
    """Create a silver tier Plan.md file based on the action file content"""
    plan_filename = f"PLAN_SILVER_{action_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    plan_path = plans_dir / plan_filename

    # Determine plan type based on action content
    if is_social_action:
        plan_type = "Social Media Integration Plan"
        plan_description = "Handle social media posting, engagement, or management tasks"
        tasks = [
            "- [ ] Analyze social media request",
            "- [ ] Determine optimal posting time",
            "- [ ] Schedule post if needed",
            "- [ ] Monitor engagement after posting",
            "- [ ] Report results"
        ]
    else:
        plan_type = "Silver Tier Integration Plan"
        plan_description = "Process multi-channel integration tasks"
        tasks = [
            "- [ ] Review multi-channel integration request",
            "- [ ] Check Gmail, WhatsApp, and LinkedIn for related items",
            "- [ ] Coordinate cross-platform response if needed",
            "- [ ] Schedule follow-up if required",
            "- [ ] Update status in system"
        ]

    # Extract relevant information from action file to create a plan
    plan_content = f"""---
created: {datetime.now().isoformat()}
status: pending_approval
action_source: {action_file.name}
tier: silver
type: {plan_type.replace(' Plan', '').lower().replace(' ', '_')}
---

# {plan_type}

## Objective
Process the request from the action file: {action_file.name}

## Context
{content[:500]}...  # First 500 characters of original content

## Plan Description
{plan_description}

## Tasks to Complete
{chr(10).join(tasks)}

## Silver Tier Specific Actions
- [ ] Coordinate between Gmail, WhatsApp, and LinkedIn channels
- [ ] Apply human-in-the-loop approval workflow if sensitive
- [ ] Schedule any time-based actions using schedule_manager
- [ ] Update MCP server status if needed

## Approval Required
- [ ] Human review and approval of this plan (if sensitive content)

## Timeline
- Started: {datetime.now().isoformat()}
- Estimated completion: [TBD based on complexity]
- Required by: [TBD - check for urgency in original request]

## Success Criteria
- [ ] Request properly addressed across relevant channels
- [ ] Appropriate follow-up scheduled or completed
- [ ] Status updated in system dashboard
- [ ] Cross-channel consistency maintained

## Notes
This plan was automatically generated by the Silver Tier Orchestrator based on the action file {action_file.name}.
This tier focuses on multi-channel integration and social media management.
"""
    plan_path.write_text(plan_content)
    logger.info(f"Created silver tier plan file: {plan_path.name}")

    # Create approval request for sensitive actions
    create_silver_approval_request(action_file, plans_dir, content)

def create_silver_approval_request(action_file: Path, plans_dir: Path, content: str):
    """Create an approval request for sensitive silver tier actions"""
    # Check if this is a sensitive action that requires approval
    requires_approval = any(keyword in content.lower() for keyword in
                           ['payment', 'invoice', 'money', 'financial', 'salary', 'confidential',
                            'private', 'sensitive', 'urgent', 'critical'])

    if requires_approval:
        approval_filename = f"APPROVAL_SILVER_{action_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        approval_path = plans_dir / "Pending_Approval" / approval_filename

        # Create Pending_Approval directory if it doesn't exist
        approval_path.parent.mkdir(exist_ok=True)

        approval_content = f"""---
type: silver_tier_approval_request
action_source: {action_file.name}
created: {datetime.now().isoformat()}
status: pending
---

# Silver Tier Approval Required

## Action Details
- **Source File:** {action_file.name}
- **Request Type:** Sensitive silver tier action requiring approval
- **Created:** {datetime.now().isoformat()}

## Silver Tier Integration Points
- [ ] Gmail integration needed
- [ ] WhatsApp integration needed
- [ ] LinkedIn integration needed
- [ ] Cross-channel coordination required

## To Approve
1. Review the original action file
2. Verify the planned response is appropriate for multi-channel handling
3. Move this file to the /Approved folder

## To Reject
Move this file to the /Rejected folder with reasons.

## Action Summary
This silver tier action involves multi-channel integration and requires human approval before proceeding.
Please review the source file and determine if the planned action is appropriate across all channels.
"""
        approval_path.write_text(approval_content)
        logger.info(f"Created silver tier approval request: {approval_path.name}")

def monitor_watchers_status(vault_path: Path):
    """Monitor the status of active watchers and log any issues"""
    logger.info("Monitoring silver tier watchers status...")

    # In a real implementation, this would check the status of running watchers
    # For now, we'll just log that this functionality exists
    status_file = vault_path / "Logs" / "watcher_status.json"
    status_file.parent.mkdir(exist_ok=True)

    # Create a basic status report
    status_report = {
        "timestamp": datetime.now().isoformat(),
        "watchers": {
            "gmail": {"status": "active", "last_check": datetime.now().isoformat()},
            "whatsapp": {"status": "active", "last_check": datetime.now().isoformat()},
            "linkedin": {"status": "active", "last_check": datetime.now().isoformat()}
        },
        "silver_tier_orchestrator": {
            "status": "active",
            "last_processed": datetime.now().isoformat(),
            "files_processed": 0
        }
    }

    status_file.write_text(json.dumps(status_report, indent=2))
    logger.info(f"Watchers status logged to {status_file}")

def main():
    vault_path = Path("../AI_Employee_Vault")

    logger.info(f"Starting silver tier orchestrator for vault: {vault_path}")

    # Create necessary directories
    (vault_path / "Needs_Action").mkdir(exist_ok=True)
    (vault_path / "Done").mkdir(exist_ok=True)
    (vault_path / "Inbox").mkdir(exist_ok=True)
    (vault_path / "Plans").mkdir(exist_ok=True)
    (vault_path / "Plans" / "Pending_Approval").mkdir(exist_ok=True)
    (vault_path / "Plans" / "Approved").mkdir(exist_ok=True)
    (vault_path / "Plans" / "Rejected").mkdir(exist_ok=True)
    (vault_path / "LinkedIn_Posts").mkdir(exist_ok=True)
    (vault_path / "Social_Posts").mkdir(exist_ok=True)
    (vault_path / "Logs").mkdir(exist_ok=True)

    # Process any existing action files in the silver tier manner
    process_needs_action_files(vault_path)

    # Monitor watcher status
    monitor_watchers_status(vault_path)

    # Update system status in dashboard
    dashboard_path = vault_path / "Dashboard.md"
    if dashboard_path.exists():
        dashboard_content = dashboard_path.read_text()
        status_marker = "## System Status"
        if status_marker in dashboard_content:
            # Find the "Last Update:" part and replace the entire line
            updated_dashboard = re.sub(
                r'Last Update:.*$',
                f'Last Update: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} (Silver Tier Orchestrator)',
                dashboard_content,
                flags=re.MULTILINE
            )
            # Update watchers status if needed
            if "- Watchers: Active" in updated_dashboard:
                # If watchers are already active, add silver tier info
                updated_dashboard = updated_dashboard.replace(
                    "- Watchers: Active",
                    "- Watchers: Active (Gmail, WhatsApp, LinkedIn)\n- Silver Tier: Active"
                )
            elif "Watchers:" in updated_dashboard:
                # Update the existing watchers status
                updated_dashboard = re.sub(
                    r'- Watchers:.*$',
                    '- Watchers: Active (Gmail, WhatsApp, LinkedIn)\n- Silver Tier: Active',
                    updated_dashboard,
                    flags=re.MULTILINE
                )
            else:
                # Add watchers status if not present
                updated_dashboard = updated_dashboard.replace(
                    "## System Status",
                    "## System Status\n- Watchers: Active (Gmail, WhatsApp, LinkedIn)\n- Silver Tier: Active"
                )

            dashboard_path.write_text(updated_dashboard)

    logger.info("Silver tier orchestrator completed one cycle")

if __name__ == "__main__":
    main()