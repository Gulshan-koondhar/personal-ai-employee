"""
Cross-Domain Integration for AI Employee

This module handles integration between personal and business domains for the Gold Tier.
"""
import time
import logging
from pathlib import Path
from datetime import datetime
import json
import sys
import os
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CrossDomainIntegrator:
    """Handles integration between personal and business domains"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.personal_dir = self.vault_path / "Personal"
        self.business_dir = self.vault_path / "Business"
        self.integration_dir = self.vault_path / "Integration"
        self.sync_dir = self.vault_path / "Sync"

        # Create necessary directories
        self.personal_dir.mkdir(exist_ok=True)
        self.business_dir.mkdir(exist_ok=True)
        self.integration_dir.mkdir(exist_ok=True)
        self.sync_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (self.personal_dir / "Finance").mkdir(exist_ok=True)
        (self.personal_dir / "Communications").mkdir(exist_ok=True)
        (self.business_dir / "Finance").mkdir(exist_ok=True)
        (self.business_dir / "Communications").mkdir(exist_ok=True)

    def detect_cross_domain_events(self) -> List[Dict[str, Any]]:
        """
        Detect events that span personal and business domains.

        Returns:
            List of cross-domain events
        """
        events = []

        # Check for business-related personal communications
        personal_emails = list((self.personal_dir / "Communications").glob("*.md"))
        for email in personal_emails:
            content = email.read_text()
            if any(keyword in content.lower() for keyword in ['client', 'project', 'invoice', 'payment', 'business']):
                events.append({
                    "type": "personal_business_overlap",
                    "source": str(email),
                    "domain": "personal_to_business",
                    "description": f"Business-related content detected in personal communication: {email.name}",
                    "severity": "medium",
                    "timestamp": datetime.now().isoformat()
                })

        # Check for personal matters in business context
        business_docs = list((self.business_dir / "Communications").glob("*.md"))
        for doc in business_docs:
            content = doc.read_text()
            if any(keyword in content.lower() for keyword in ['personal', 'family', 'vacation', 'doctor', 'appointment']):
                events.append({
                    "type": "business_personal_overlap",
                    "source": str(doc),
                    "domain": "business_to_personal",
                    "description": f"Personal matter detected in business communication: {doc.name}",
                    "severity": "medium",
                    "timestamp": datetime.now().isoformat()
                })

        # Check for financial transactions that span domains
        personal_finance = list((self.personal_dir / "Finance").glob("*.md"))
        business_finance = list((self.business_dir / "Finance").glob("*.md"))

        for p_fin in personal_finance:
            p_content = p_fin.read_text()
            if 'business' in p_content.lower() or 'work' in p_content.lower():
                events.append({
                    "type": "finance_cross_domain",
                    "source": str(p_fin),
                    "domain": "personal_to_business",
                    "description": f"Business-related finance in personal records: {p_fin.name}",
                    "severity": "high",
                    "timestamp": datetime.now().isoformat()
                })

        for b_fin in business_finance:
            b_content = b_fin.read_text()
            if 'personal' in b_content.lower() or 'private' in b_content.lower():
                events.append({
                    "type": "finance_cross_domain",
                    "source": str(b_fin),
                    "domain": "business_to_personal",
                    "description": f"Personal finance in business records: {b_fin.name}",
                    "severity": "high",
                    "timestamp": datetime.now().isoformat()
                })

        return events

    def create_cross_domain_link(self, from_domain: str, to_domain: str,
                                 from_file: str, to_file: str, link_type: str) -> str:
        """
        Create a cross-domain link between files.

        Args:
            from_domain: Source domain ('personal' or 'business')
            to_domain: Target domain ('personal' or 'business')
            from_file: Source file path
            to_file: Target file path
            link_type: Type of link ('related_to', 'depends_on', 'affects', etc.)

        Returns:
            Link ID
        """
        link_id = f"link_{int(time.time() * 1000)}"

        # Create a link record
        link_data = {
            "link_id": link_id,
            "timestamp": datetime.now().isoformat(),
            "from_domain": from_domain,
            "to_domain": to_domain,
            "from_file": from_file,
            "to_file": to_file,
            "link_type": link_type,
            "created_by": "cross_domain_integrator"
        }

        # Save the link record
        link_filename = f"LINK_{from_domain}_to_{to_domain}_{link_id}.json"
        link_path = self.integration_dir / link_filename

        with open(link_path, 'w', encoding='utf-8') as f:
            json.dump(link_data, f, indent=2)

        logger.info(f"Cross-domain link created: {link_data}")
        return link_id

    def sync_personal_business_tasks(self) -> Dict[str, Any]:
        """
        Synchronize tasks that span personal and business domains.

        Returns:
            Dictionary with synchronization results
        """
        results = {
            "personal_to_business": [],
            "business_to_personal": [],
            "conflicts": [],
            "synchronized": 0
        }

        # Look for personal tasks that mention business
        personal_tasks = list(self.personal_dir.rglob("*task*.md"))
        for task in personal_tasks:
            content = task.read_text()
            if any(keyword in content.lower() for keyword in ['client', 'meeting', 'work', 'office', 'project']):
                # This personal task may affect business - create a reference
                business_ref = self._create_business_ref_from_personal(task, content)
                results["personal_to_business"].append({
                    "personal_task": str(task),
                    "business_ref": business_ref
                })
                results["synchronized"] += 1

        # Look for business tasks that mention personal
        business_tasks = list(self.business_dir.rglob("*task*.md"))
        for task in business_tasks:
            content = task.read_text()
            if any(keyword in content.lower() for keyword in ['personal', 'family', 'vacation', 'appointment', 'private']):
                # This business task may affect personal - create a reference
                personal_ref = self._create_personal_ref_from_business(task, content)
                results["business_to_personal"].append({
                    "business_task": str(task),
                    "personal_ref": personal_ref
                })
                results["synchronized"] += 1

        # Check for potential conflicts
        results["conflicts"] = self._detect_schedule_conflicts()

        return results

    def _create_business_ref_from_personal(self, personal_task: Path, content: str) -> str:
        """Create a business reference from a personal task."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ref_file = self.business_dir / f"BUSINESS_REF_{timestamp}_{personal_task.name}"

        ref_content = f"""---
type: business_reference
source_domain: personal
original_file: {str(personal_task)}
created_at: {datetime.now().isoformat()}
---

# Business Reference from Personal Task

## Original Content
{content}

## Cross-Domain Impact
This business reference was automatically generated from a personal task that mentions business activities.

## Actions Required
- [ ] Review business impact
- [ ] Schedule accordingly
- [ ] Update business calendar if needed

## Synchronization
This item is synchronized between personal and business domains.
"""
        ref_file.write_text(ref_content)
        return str(ref_file)

    def _create_personal_ref_from_business(self, business_task: Path, content: str) -> str:
        """Create a personal reference from a business task."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ref_file = self.personal_dir / f"PERSONAL_REF_{timestamp}_{business_task.name}"

        ref_content = f"""---
type: personal_reference
source_domain: business
original_file: {str(business_task)}
created_at: {datetime.now().isoformat()}
---

# Personal Reference from Business Task

## Original Content
{content}

## Cross-Domain Impact
This personal reference was automatically generated from a business task that affects personal scheduling.

## Actions Required
- [ ] Review personal impact
- [ ] Adjust personal calendar if needed
- [ ] Consider rescheduling if conflicts exist

## Synchronization
This item is synchronized between business and personal domains.
"""
        ref_file.write_text(ref_content)
        return str(ref_file)

    def _detect_schedule_conflicts(self) -> List[Dict[str, Any]]:
        """Detect potential schedule conflicts between domains."""
        conflicts = []

        # This is a simplified detection - in reality, this would parse calendar events
        # and check for time conflicts
        personal_schedule = list((self.personal_dir / "Schedule").glob("*.md")) if (self.personal_dir / "Schedule").exists() else []
        business_schedule = list((self.business_dir / "Schedule").glob("*.md")) if (self.business_dir / "Schedule").exists() else []

        # For demo purposes, just return empty conflicts
        # In real implementation, this would parse event times and identify overlaps
        return conflicts

    def create_integration_dashboard(self) -> Path:
        """
        Create a dashboard showing cross-domain integration status.

        Returns:
            Path to the integration dashboard file
        """
        dashboard_path = self.integration_dir / f"Integration_Dashboard_{datetime.now().strftime('%Y%m%d')}.md"

        # Gather integration statistics
        cross_events = self.detect_cross_domain_events()
        sync_results = self.sync_personal_business_tasks()

        dashboard_content = f"""---
type: integration_dashboard
generated: {datetime.now().isoformat()}
---

# Cross-Domain Integration Dashboard

## Executive Summary
This dashboard shows the integration status between personal and business domains.
**{len(cross_events)} cross-domain events** detected and **{sync_results['synchronized']} items synchronized**.

## Cross-Domain Events ({len(cross_events)})
"""
        for event in cross_events:
            domain_icon = "BUS_to_PERS" if "personal_to_business" in event['domain'] else "PERS_to_BUS"
            severity_icon = "HIGH" if event['severity'] == 'high' else "MED"
            dashboard_content += f"- [{domain_icon}] [{severity_icon}] {event['description']}\n"

        dashboard_content += f"""

## Task Synchronization ({sync_results['synchronized']} synchronized)
- Personal to Business: {len(sync_results['personal_to_business'])} references created
- Business to Personal: {len(sync_results['business_to_personal'])} references created

## Schedule Conflicts
- Detected conflicts: {len(sync_results['conflicts'])}

## Integration Health
- Cross-domain awareness: {'Active' if cross_events else 'None detected'}
- Task synchronization: {'Active' if sync_results['synchronized'] > 0 else 'Inactive'}
- Conflict detection: {'Active' if sync_results['conflicts'] else 'None detected'}

## Last Updated
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Action Items
- Review cross-domain events for potential issues
- Ensure synchronized tasks are properly managed
- Address any detected schedule conflicts

---
*This dashboard was automatically generated by the Cross-Domain Integration system.*
"""
        dashboard_path.write_text(dashboard_content)
        return dashboard_path

    def process_cross_domain_notification(self, notification_data: Dict[str, Any]) -> bool:
        """
        Process a notification that spans domains.

        Args:
            notification_data: Dictionary with notification details

        Returns:
            True if successfully processed, False otherwise
        """
        try:
            # Determine if this notification affects both domains
            affects_both_domains = any(
                keyword in notification_data.get('content', '').lower()
                for keyword in ['business', 'work', 'personal', 'client', 'private']
            )

            if affects_both_domains:
                # Create references in both domains
                self._create_domain_references(notification_data)

                # Log the cross-domain action
                logger.info(f"Cross-domain notification processed: {notification_data}")
                return True

            return False  # Only affected one domain
        except Exception as e:
            logger.error(f"Error processing cross-domain notification: {e}")
            return False

    def _create_domain_references(self, notification_data: Dict[str, Any]):
        """Create references to a notification in both domains."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Create reference in personal domain
        personal_ref = self.personal_dir / f"DOMAIN_REF_{timestamp}_{notification_data.get('id', 'unknown')}.md"
        personal_content = f"""---
type: domain_reference
domain: personal
original_source: {notification_data.get('source', 'unknown')}
created_at: {datetime.now().isoformat()}
---

# Domain Reference: {notification_data.get('title', 'Cross-Domain Notification')}

## From Business Domain
A notification from the business domain requires personal attention.

## Original Content
{notification_data.get('content', '')}

## Actions Required
- [ ] Review personal implications
- [ ] Adjust personal schedule if needed
- [ ] Respond appropriately
"""
        personal_ref.write_text(personal_content)

        # Create reference in business domain
        business_ref = self.business_dir / f"DOMAIN_REF_{timestamp}_{notification_data.get('id', 'unknown')}.md"
        business_content = f"""---
type: domain_reference
domain: business
original_source: {notification_data.get('source', 'unknown')}
created_at: {datetime.now().isoformat()}
---

# Domain Reference: {notification_data.get('title', 'Cross-Domain Notification')}

## From Personal Domain
A notification from the personal domain requires business attention.

## Original Content
{notification_data.get('content', '')}

## Actions Required
- [ ] Review business implications
- [ ] Adjust business schedule if needed
- [ ] Respond appropriately
"""
        business_ref.write_text(business_content)

def main():
    """Main function to demonstrate cross-domain integration"""
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure if needed
    (vault_path / "Personal" / "Communications").mkdir(parents=True, exist_ok=True)
    (vault_path / "Business" / "Communications").mkdir(parents=True, exist_ok=True)

    integrator = CrossDomainIntegrator(str(vault_path))

    # Create some sample files that demonstrate cross-domain overlap
    print("Creating sample cross-domain files...")

    # Personal file with business content
    personal_business_file = vault_path / "Personal" / "Communications" / "client_email.md"
    personal_business_file.write_text("""# Client Communication

Subject: Project Update Request
From: client@business.com

Could you please provide an update on the project status?
This is important for our Q1 deliverables.
""")

    # Business file with personal content
    business_personal_file = vault_path / "Business" / "Communications" / "vacation_notice.md"
    business_personal_file.write_text("""# Internal Notice

Subject: Vacation Request
From: employee@company.com

I will be on personal vacation from March 1-5.
Please handle any urgent matters during this period.
""")

    # Detect cross-domain events
    print("Detecting cross-domain events...")
    events = integrator.detect_cross_domain_events()
    print(f"Detected {len(events)} cross-domain events:")
    for event in events:
        print(f"  - {event['description']}")

    # Synchronize tasks
    print("\nSynchronizing cross-domain tasks...")
    sync_results = integrator.sync_personal_business_tasks()
    print(f"Synchronized {sync_results['synchronized']} items")

    # Create integration dashboard
    print("\nCreating integration dashboard...")
    dashboard_path = integrator.create_integration_dashboard()
    print(f"Dashboard created: {dashboard_path}")

    # Process a cross-domain notification
    print("\nProcessing cross-domain notification...")
    notification = {
        "id": "not_123",
        "title": "Schedule Conflict",
        "content": "Important client meeting conflicts with personal appointment",
        "source": "calendar"
    }
    processed = integrator.process_cross_domain_notification(notification)
    print(f"Notification processed: {processed}")

    print("\nCross-domain integration demo completed!")

if __name__ == "__main__":
    main()