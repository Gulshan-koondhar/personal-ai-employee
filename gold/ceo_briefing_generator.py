"""
CEO Briefing Generator for AI Employee

This module generates weekly business and accounting audits with CEO briefings for the Gold Tier.
"""
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
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

class CEOBriefingGenerator:
    """Generates weekly business and accounting audits with CEO briefings"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.reports_dir = self.vault_path / "Reports"
        self.briefings_dir = self.vault_path / "Briefings"
        self.tasks_dir = self.vault_path / "Tasks"

        # Create necessary directories
        self.reports_dir.mkdir(exist_ok=True)
        self.briefings_dir.mkdir(exist_ok=True)
        self.tasks_dir.mkdir(exist_ok=True)

    def generate_weekly_audit(self, week_start: str = None) -> Dict[str, Any]:
        """
        Generate a weekly business and accounting audit.

        Args:
            week_start: Start date of the week in YYYY-MM-DD format (defaults to last Monday)

        Returns:
            Dictionary with audit data
        """
        if not week_start:
            # Calculate last Monday
            today = datetime.now()
            days_since_monday = (today.weekday())  # Monday is 0
            last_monday = today - timedelta(days=days_since_monday)
            week_start = last_monday.strftime('%Y-%m-%d')

        # Parse the date
        start_date = datetime.strptime(week_start, '%Y-%m-%d')
        end_date = start_date + timedelta(days=6)  # 7 days total

        period = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"

        logger.info(f"Generating weekly audit for period: {period}")

        # Calculate metrics (this would normally analyze real data)
        audit_data = {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "week_start": week_start,
            "revenue": self._calculate_revenue(start_date, end_date),
            "expenses": self._calculate_expenses(start_date, end_date),
            "profit": 0,
            "completed_tasks": self._get_completed_tasks(start_date, end_date),
            "pending_tasks": self._get_pending_tasks(),
            "bottlenecks": self._identify_bottlenecks(),
            "upcoming_deadlines": self._get_upcoming_deadlines(),
            "subscription_costs": self._analyze_subscriptions(),
            "client_metrics": self._get_client_metrics(),
            "recommendations": self._generate_recommendations()
        }

        # Calculate profit
        audit_data["profit"] = audit_data["revenue"]["total"] - audit_data["expenses"]["total"]

        # Create the audit report file
        report_filename = f"Weekly_Audit_{week_start.replace('-', '')}.md"
        report_path = self.reports_dir / report_filename

        report_content = self._format_audit_report(audit_data)
        report_path.write_text(report_content)

        return audit_data

    def _calculate_revenue(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate revenue for the period (simulated)."""
        # In real implementation, this would analyze invoices/payouts
        # For demo, we'll simulate some data
        invoices = [
            {"amount": 2500, "client": "Client A", "date": "2026-02-15", "status": "paid"},
            {"amount": 1800, "client": "Client B", "date": "2026-02-16", "status": "paid"},
            {"amount": 3200, "client": "Client C", "date": "2026-02-17", "status": "pending"}
        ]

        total = sum(inv["amount"] for inv in invoices if inv["status"] == "paid")

        return {
            "total": total,
            "breakdown": invoices,
            "paid_invoices": len([inv for inv in invoices if inv["status"] == "paid"]),
            "pending_invoices": len([inv for inv in invoices if inv["status"] == "pending"])
        }

    def _calculate_expenses(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Calculate expenses for the period (simulated)."""
        # In real implementation, this would analyze expenses
        expenses = [
            {"amount": 350, "category": "Software", "description": "Monthly subscription fees", "date": "2026-02-15"},
            {"amount": 120, "category": "Utilities", "description": "Internet and phone", "date": "2026-02-16"},
            {"amount": 85, "category": "Office", "description": "Supplies", "date": "2026-02-17"},
            {"amount": 950, "category": "Marketing", "description": "Ad spend", "date": "2026-02-18"}
        ]

        total = sum(exp["amount"] for exp in expenses)

        return {
            "total": total,
            "breakdown": expenses,
            "by_category": self._summarize_by_category(expenses)
        }

    def _summarize_by_category(self, expenses: List[Dict]) -> Dict[str, float]:
        """Summarize expenses by category."""
        summary = {}
        for exp in expenses:
            cat = exp["category"]
            summary[cat] = summary.get(cat, 0) + exp["amount"]
        return summary

    def _get_completed_tasks(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get completed tasks for the period (simulated)."""
        # In real implementation, this would analyze task completion data
        return [
            {"task": "Client A project milestone 1", "completed_date": "2026-02-15", "assignee": "Team Alpha"},
            {"task": "Monthly report preparation", "completed_date": "2026-02-16", "assignee": "AI Employee"},
            {"task": "Software update deployment", "completed_date": "2026-02-17", "assignee": "Dev Team"},
            {"task": "Client B proposal", "completed_date": "2026-02-18", "assignee": "Sales Team"}
        ]

    def _get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get pending tasks (simulated)."""
        return [
            {"task": "Client C project delivery", "due_date": "2026-02-25", "priority": "high"},
            {"task": "Quarterly budget planning", "due_date": "2026-03-01", "priority": "medium"},
            {"task": "New tool evaluation", "due_date": "2026-03-10", "priority": "low"}
        ]

    def _identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify potential bottlenecks (simulated)."""
        return [
            {
                "task": "Client C project",
                "issue": "Resource allocation conflict",
                "impact": "Potential 2-day delay",
                "suggestion": "Reallocate resources from lower priority project"
            },
            {
                "task": "Software deployment",
                "issue": "Dependency on external vendor",
                "impact": "Waiting on API integration",
                "suggestion": "Follow up with vendor immediately"
            }
        ]

    def _get_upcoming_deadlines(self) -> List[Dict[str, Any]]:
        """Get upcoming deadlines (simulated)."""
        return [
            {"project": "Client A final delivery", "due_date": "2026-02-25", "days_remaining": 6},
            {"project": "Q1 tax prep", "due_date": "2026-03-31", "days_remaining": 39},
            {"project": "Contract renewal", "due_date": "2026-03-15", "days_remaining": 24}
        ]

    def _analyze_subscriptions(self) -> List[Dict[str, Any]]:
        """Analyze subscription costs (simulated)."""
        return [
            {"service": "Cloud Storage", "cost": 50, "status": "active", "last_activity": "2026-02-18"},
            {"service": "Project Management Tool", "cost": 150, "status": "active", "last_activity": "2026-02-18"},
            {"service": "Analytics Platform", "cost": 200, "status": "active", "last_activity": "2026-02-17"},
            {"service": "Unused Service", "cost": 75, "status": "low_activity", "last_activity": "2026-01-15"}
        ]

    def _get_client_metrics(self) -> Dict[str, Any]:
        """Get client-related metrics (simulated)."""
        return {
            "active_clients": 12,
            "new_inquiries": 3,
            "response_time_avg_hours": 4.2,
            "satisfaction_score": 4.6,
            "revenue_per_client_avg": 2100
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate business recommendations (simulated)."""
        return [
            "Consider canceling 'Unused Service' subscription to save $75/month",
            "Investigate the Client C project bottleneck to prevent delays",
            "The response time of 4.2 hours is above the target of 24 hours - consider additional support",
            "Client satisfaction score of 4.6/5 is good, but room for improvement"
        ]

    def _format_audit_report(self, audit_data: Dict[str, Any]) -> str:
        """Format the audit report in Markdown."""
        report = f"""---
type: weekly_audit
period: {audit_data['period']}
generated: {audit_data['generated_at']}
---

# Weekly Business and Accounting Audit

## Executive Summary
This week showed **strong revenue performance** with ${audit_data['revenue']['total']:,} in collected revenue against ${audit_data['expenses']['total']:,} in expenses, resulting in a net profit of ${audit_data['profit']:,}. **{len(audit_data['completed_tasks'])} tasks** were completed successfully. One bottleneck identified that may impact upcoming deadlines.

## Revenue Analysis
- **Total Revenue:** ${audit_data['revenue']['total']:,}
- **Paid Invoices:** {audit_data['revenue']['paid_invoices']}
- **Pending Invoices:** {audit_data['revenue']['pending_invoices']}
- **Top Clients:**
"""
        for inv in audit_data['revenue']['breakdown']:
            status_icon = "[PAID]" if inv['status'] == 'paid' else "[PENDING]"
            report += f"  - {status_icon} ${inv['amount']:,} from {inv['client']} ({inv['status']})\n"

        report += f"""

## Expense Analysis
- **Total Expenses:** ${audit_data['expenses']['total']:,}
- **By Category:**
"""
        for cat, amount in audit_data['expenses']['by_category'].items():
            report += f"  - {cat}: ${amount:,}\n"

        report += f"""

## Completed Tasks ({len(audit_data['completed_tasks'])})
"""
        for task in audit_data['completed_tasks']:
            report += f"- [DONE] {task['task']} (completed: {task['completed_date']}, by: {task['assignee']})\n"

        report += f"""

## Pending Tasks ({len(audit_data['pending_tasks'])})
"""
        for task in audit_data['pending_tasks']:
            report += f"- [PENDING] {task['task']} (due: {task['due_date']}, priority: {task['priority']})\n"

        report += f"""

## Bottlenecks Identified ({len(audit_data['bottlenecks'])})
"""
        for bottleneck in audit_data['bottlenecks']:
            report += f"- [CRITICAL] {bottleneck['task']}: {bottleneck['issue']} (Impact: {bottleneck['impact']})\n"
            report += f"  - Suggestion: {bottleneck['suggestion']}\n"

        report += f"""

## Upcoming Deadlines ({len(audit_data['upcoming_deadlines'])})
"""
        for deadline in audit_data['upcoming_deadlines']:
            report += f"- [CALENDAR] {deadline['project']} due {deadline['due_date']} ({deadline['days_remaining']} days)\n"

        report += f"""

## Subscription Audit ({len(audit_data['subscription_costs'])} subscriptions)
"""
        for sub in audit_data['subscription_costs']:
            status_icon = "[ACTIVE]" if sub['status'] == 'active' else "[INACTIVE]"
            report += f"- {status_icon} {sub['service']}: ${sub['cost']}/mo (last activity: {sub['last_activity']})\n"

        report += f"""

## Client Metrics
- Active Clients: {audit_data['client_metrics']['active_clients']}
- New Inquiries: {audit_data['client_metrics']['new_inquiries']}
- Avg Response Time: {audit_data['client_metrics']['response_time_avg_hours']} hours
- Satisfaction Score: {audit_data['client_metrics']['satisfaction_score']}/5.0
- Avg Revenue per Client: ${audit_data['client_metrics']['revenue_per_client_avg']:,}

## Proactive Recommendations
"""
        for i, rec in enumerate(audit_data['recommendations'], 1):
            report += f"{i}. [RECOMMENDATION] {rec}\n"

        report += f"""

---
*Generated by AI Employee on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return report

    def generate_ceo_briefing(self, week_start: str = None) -> Path:
        """
        Generate a CEO-level briefing based on the weekly audit data.

        Args:
            week_start: Start date of the week in YYYY-MM-DD format

        Returns:
            Path to the generated briefing file
        """
        # First, generate the audit if it doesn't exist
        audit_data = self.generate_weekly_audit(week_start)

        briefing_filename = f"CEO_Briefing_{audit_data['week_start'].replace('-', '')}.md"
        briefing_path = self.briefings_dir / briefing_filename

        briefing_content = self._format_ceo_briefing(audit_data)
        briefing_path.write_text(briefing_content)

        logger.info(f"CEO briefing generated: {briefing_path.name}")
        return briefing_path

    def _format_ceo_briefing(self, audit_data: Dict[str, Any]) -> str:
        """Format the CEO briefing in Markdown."""
        briefing = f"""---
type: ceo_briefing
period: {audit_data['period']}
generated: {audit_data['generated_at']}
---

# Monday Morning CEO Briefing

## Executive Summary
**Strong week with ${audit_data['revenue']['total']:,} in revenue**. {len(audit_data['completed_tasks'])} tasks completed. **One critical bottleneck** requires immediate attention to prevent project delays.

## Financial Performance
- **Revenue:** ${audit_data['revenue']['total']:,} ({'+' if audit_data['profit'] > 0 else ''}${audit_data['profit']:,} profit)
- **Expenses:** ${audit_data['expenses']['total']:,}
- **Outstanding:** ${sum(inv['amount'] for inv in audit_data['revenue']['breakdown'] if inv['status'] == 'pending'):,}

## Key Highlights
- {len(audit_data['completed_tasks'])} tasks completed successfully
- Client satisfaction at solid {audit_data['client_metrics']['satisfaction_score']}/5.0
- {audit_data['client_metrics']['active_clients']} active clients generating value

## Critical Issues
"""
        for bottleneck in audit_data['bottlenecks']:
            briefing += f"- [WARNING] {bottleneck['task']}: {bottleneck['issue']}\n"
            briefing += f"  - *Impact:* {bottleneck['impact']}\n"

        briefing += "\n## Upcoming Focus Areas\n"
        for rec in audit_data['recommendations'][:3]:  # Top 3 recommendations
            briefing += f"- {rec}\n"

        briefing += f"\n## This Week's Priorities\n"
        for deadline in audit_data['upcoming_deadlines']:
            if deadline['days_remaining'] <= 14:  # Only show deadlines within 2 weeks
                briefing += f"- {deadline['project']} due in {deadline['days_remaining']} days\n"

        briefing += f"""

## Weekly Trend Analysis
- Revenue trend: {'UP' if audit_data['revenue']['total'] > 1000 else 'STABLE'}
- Expense control: {'GOOD' if audit_data['expenses']['total'] < 1500 else 'MONITOR'}
- Client satisfaction: {'POSITIVE' if audit_data['client_metrics']['satisfaction_score'] > 4.0 else 'NEEDS_ATTENTION'}

## Immediate Actions Required
1. Address the Client C project bottleneck immediately
2. Review pending invoices for follow-up
3. Consider subscription audit recommendation

---
*Generated automatically by AI Employee. Available for detailed analysis and task management.*
"""
        return briefing

def main():
    """Main function to demonstrate CEO briefing generation"""
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure if needed
    (vault_path / "Reports").mkdir(exist_ok=True)
    (vault_path / "Briefings").mkdir(exist_ok=True)

    generator = CEOBriefingGenerator(str(vault_path))

    # Generate a weekly audit and CEO briefing
    print("Generating weekly audit...")
    audit_data = generator.generate_weekly_audit()
    print(f"Weekly audit completed: {audit_data['period']}")

    print("\nGenerating CEO briefing...")
    briefing_path = generator.generate_ceo_briefing()
    print(f"CEO briefing generated: {briefing_path}")

    # Show some key metrics
    print(f"\nKey Metrics:")
    print(f"- Revenue: ${audit_data['revenue']['total']:,}")
    print(f"- Expenses: ${audit_data['expenses']['total']:,}")
    print(f"- Profit: ${audit_data['profit']:,}")
    print(f"- Completed tasks: {len(audit_data['completed_tasks'])}")

    print("\nCEO Briefing Generator demo completed!")

if __name__ == "__main__":
    main()