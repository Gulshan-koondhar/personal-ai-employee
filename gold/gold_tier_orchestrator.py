"""
Gold Tier Orchestrator for AI Employee

This orchestrator implements all Gold Tier features including:
- Ralph Wiggum loops for persistence
- Cross-domain integration
- Comprehensive audit logging
- Error recovery and graceful degradation
- CEO briefing generation
- Multiple MCP server coordination
"""
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json
import sys
import os

# Import Gold Tier components
from ralph_wiggum_loop import RalphWiggumLoop
from audit_logger import AuditLogger
from error_recovery import ErrorRecoveryManager, error_handling_context
from ceo_briefing_generator import CEOBriefingGenerator
from cross_domain_integration import CrossDomainIntegrator
from social_integration import SocialMediaIntegrator
from twitter_integration import TwitterIntegrator
from agent_skills.email_skill import send_email, queue_email_for_approval
from agent_skills.file_processing_skill import create_action_file, create_plan_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoldTierOrchestrator:
    """Main orchestrator for all Gold Tier features"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.plans = self.vault_path / "Plans"

        # Initialize Gold Tier components
        self.ralph_loop = RalphWiggumLoop(str(vault_path))
        self.audit_logger = AuditLogger(str(vault_path))
        self.error_recovery = ErrorRecoveryManager(str(vault_path))
        self.briefing_generator = CEOBriefingGenerator(str(vault_path))
        self.cross_domain = CrossDomainIntegrator(str(vault_path))
        self.social = SocialMediaIntegrator(str(vault_path))
        self.twitter = TwitterIntegrator(str(vault_path))

        # Create necessary directories
        self.needs_action.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.plans.mkdir(exist_ok=True)

    def process_with_ralph_wiggum_loop(self, initial_prompt: str, task_id: str):
        """
        Process tasks using Ralph Wiggum loop for persistence.
        """
        logger.info(f"Starting Ralph Wiggum loop for task: {task_id}")

        self.audit_logger.log_event(
            event_type="ralph_loop_start",
            description=f"Starting Ralph Wiggum loop for task {task_id}",
            actor="orchestrator",
            result="success",
            parameters={"task_id": task_id, "prompt": initial_prompt}
        )

        try:
            result = self.ralph_loop.run_loop(initial_prompt, task_id)

            self.audit_logger.log_event(
                event_type="ralph_loop_complete",
                description=f"Completed Ralph Wiggum loop for task {task_id}",
                actor="orchestrator",
                result="success",
                parameters={"task_id": task_id, "result": result}
            )

            return result
        except Exception as e:
            error_id = self.error_recovery.log_error(
                e, f"Error in Ralph Wiggum loop for task {task_id}", "high"
            )

            self.audit_logger.log_event(
                event_type="ralph_loop_error",
                description=f"Error in Ralph Wiggum loop: {error_id}",
                actor="orchestrator",
                result="failed",
                parameters={"task_id": task_id, "error_id": error_id}
            )

            raise e

    def process_needs_action_with_gold_features(self):
        """Process all Needs_Action files with all Gold Tier features."""
        logger.info("Starting Gold Tier processing of Needs_Action files")

        # Cross-domain integration check
        cross_events = self.cross_domain.detect_cross_domain_events()
        for event in cross_events:
            self.audit_logger.log_event(
                event_type="cross_domain_event",
                description=event['description'],
                actor="cross_domain_detector",
                result="detected",
                parameters=event
            )

        # Process each action file
        action_files = list(self.needs_action.glob("*.md"))

        processed_count = 0
        for action_file in action_files:
            if action_file.name.startswith('.'):
                continue  # Skip hidden files

            logger.info(f"Processing action file: {action_file.name}")

            with error_handling_context(self.error_recovery, f"Processing {action_file.name}"):
                try:
                    # Log the start of processing
                    self.audit_logger.log_event(
                        event_type="action_processing_start",
                        description=f"Starting processing of {action_file.name}",
                        actor="orchestrator",
                        result="in_progress",
                        target=str(action_file)
                    )

                    # Read the action file
                    content = action_file.read_text()

                    # Create a plan based on the action
                    plan_result = self.error_recovery.graceful_degrade(
                        lambda: create_plan_file(
                            objective=f"Process action file: {action_file.name}",
                            tasks=["Review content", "Determine appropriate action", "Execute action", "Update status"],
                            timeline="24 hours"
                        ),
                        lambda: create_plan_file(
                            objective=f"Process action file: {action_file.name}",
                            tasks=["Review content", "Update status"],
                            timeline="48 hours"
                        ),
                        f"Creating plan for {action_file.name}"
                    )

                    # Check if this is a cross-domain request
                    if any(keyword in content.lower() for keyword in ['personal', 'business', 'work', 'family']):
                        self.cross_domain.process_cross_domain_notification({
                            "id": action_file.stem,
                            "title": f"Action: {action_file.name}",
                            "content": content[:200] + "..." if len(content) > 200 else content,
                            "source": str(action_file)
                        })

                    # Check for social media requests
                    if any(keyword in content.lower() for keyword in ['facebook', 'instagram', 'social', 'post', 'tweet', 'twitter']):
                        self._handle_social_media_request(content, action_file)

                    # Move to Done folder
                    done_file = self.done / action_file.name

                    # Handle case where file already exists in Done folder
                    if done_file.exists():
                        # Add timestamp to make unique
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                        done_file = self.done / f"{action_file.stem}_{timestamp}{action_file.suffix}"

                    action_file.rename(done_file)

                    # Log successful completion
                    self.audit_logger.log_event(
                        event_type="action_processing_success",
                        description=f"Successfully processed {action_file.name}",
                        actor="orchestrator",
                        result="success",
                        target=str(done_file)
                    )

                    processed_count += 1

                except Exception as e:
                    # Log error and save failed action
                    error_id = self.error_recovery.log_error(
                        e, f"Error processing {action_file.name}", "high"
                    )

                    # Save failed action for later processing
                    failed_action_data = {
                        "id": action_file.stem,
                        "original_path": str(action_file),
                        "error_id": error_id,
                        "timestamp": datetime.now().isoformat()
                    }

                    self.error_recovery.save_failed_action(failed_action_data, {
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "timestamp": datetime.now().isoformat()
                    })

                    # Log the failure
                    self.audit_logger.log_event(
                        event_type="action_processing_failed",
                        description=f"Failed to process {action_file.name}",
                        actor="orchestrator",
                        result="failed",
                        target=str(action_file),
                        parameters={"error_id": error_id}
                    )

        # Process any previously failed actions
        recovery_results = self.error_recovery.process_failed_actions()
        logger.info(f"Failed action recovery results: {recovery_results}")

        return processed_count

    def _handle_social_media_request(self, content: str, source_file: Path):
        """Handle social media related requests from action files."""
        try:
            if 'twitter' in content.lower() or 'x' in content.lower():
                # Create a Twitter post
                self.twitter.create_tweet(content[:280])
            elif 'facebook' in content.lower():
                # Create a Facebook post
                self.social.create_facebook_post(content)
            elif 'instagram' in content.lower():
                # Create an Instagram post
                self.social.create_instagram_post(content, "images/default_social_image.jpg")
            else:
                # Default to creating a general social post
                self.social.create_facebook_post(content)

            logger.info(f"Created social media post from {source_file.name}")
        except Exception as e:
            logger.error(f"Error creating social media post: {e}")

    def generate_weekly_ceo_briefing(self):
        """Generate the weekly CEO briefing."""
        logger.info("Generating weekly CEO briefing")

        try:
            briefing_path = self.briefing_generator.generate_ceo_briefing()
            logger.info(f"CEO briefing generated: {briefing_path}")

            self.audit_logger.log_event(
                event_type="ceo_briefing_generated",
                description="Weekly CEO briefing generated",
                actor="briefing_generator",
                result="success",
                target=str(briefing_path)
            )
        except Exception as e:
            error_id = self.error_recovery.log_error(
                e, "Error generating CEO briefing", "high"
            )
            logger.error(f"Failed to generate CEO briefing: {error_id}")

    def generate_integration_dashboard(self):
        """Generate the cross-domain integration dashboard."""
        logger.info("Generating integration dashboard")

        try:
            dashboard_path = self.cross_domain.create_integration_dashboard()
            logger.info(f"Integration dashboard generated: {dashboard_path}")

            self.audit_logger.log_event(
                event_type="integration_dashboard_generated",
                description="Cross-domain integration dashboard generated",
                actor="cross_domain_integrator",
                result="success",
                target=str(dashboard_path)
            )
        except Exception as e:
            error_id = self.error_recovery.log_error(
                e, "Error generating integration dashboard", "medium"
            )
            logger.error(f"Failed to generate integration dashboard: {error_id}")

    def perform_system_health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive system health check."""
        logger.info("Performing system health check")

        health_results = {
            "timestamp": datetime.now().isoformat(),
            "component_health": {},
            "overall_status": "unknown",
            "issues_found": 0
        }

        # Check each component
        try:
            # Health check for error recovery system
            health_results["component_health"]["error_recovery"] = self.error_recovery.health_check()

            # Check directories
            directories = {
                "Needs_Action": self.needs_action,
                "Done": self.done,
                "Plans": self.plans,
                "Logs": self.vault_path / "Logs",
                "Briefings": self.vault_path / "Briefings"
            }

            dir_health = {}
            for name, path in directories.items():
                dir_health[name] = {
                    "exists": path.exists(),
                    "writable": self._is_writable(path),
                    "file_count": len(list(path.glob("*"))) if path.exists() else 0
                }

            health_results["component_health"]["directories"] = dir_health

            # Check for any issues
            issues = []
            for component, status in health_results["component_health"].items():
                if isinstance(status, dict):
                    if status.get("overall_status") == "degraded":
                        issues.append(f"{component} is degraded")
                    if status.get("recent_errors_count", 0) > 5:
                        issues.append(f"High error count in {component}")

            health_results["issues_found"] = len(issues)
            health_results["overall_status"] = "degraded" if issues else "healthy"
            health_results["issues"] = issues

            # Log the health check
            self.audit_logger.log_event(
                event_type="system_health_check",
                description=f"System health check completed: {health_results['overall_status']}",
                actor="orchestrator",
                result="success",
                parameters=health_results
            )

        except Exception as e:
            error_id = self.error_recovery.log_error(
                e, "Error during system health check", "high"
            )
            logger.error(f"Health check error: {error_id}")
            health_results["overall_status"] = "error"
            health_results["error_id"] = error_id

        return health_results

    def _is_writable(self, path: Path) -> bool:
        """Check if a directory is writable."""
        try:
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
            return True
        except:
            return False

    def run_complete_gold_tier_cycle(self):
        """Run a complete cycle of all Gold Tier features."""
        logger.info("Starting complete Gold Tier processing cycle")

        # Log the start of the cycle
        self.audit_logger.log_event(
            event_type="gold_tier_cycle_start",
            description="Starting complete Gold Tier processing cycle",
            actor="orchestrator",
            result="in_progress"
        )

        results = {
            "processed_actions": 0,
            "created_plans": 0,
            "handled_cross_domain": 0,
            "generated_briefings": False,
            "created_dashboards": False,
            "health_check_result": None
        }

        try:
            # Process action files with all Gold Tier features
            results["processed_actions"] = self.process_needs_action_with_gold_features()

            # Generate weekly CEO briefing (only if it's Monday)
            if datetime.now().weekday() == 0:  # Monday
                self.generate_weekly_ceo_briefing()
                results["generated_briefings"] = True

            # Generate integration dashboard
            self.generate_integration_dashboard()
            results["created_dashboards"] = True

            # Perform system health check
            results["health_check_result"] = self.perform_system_health_check()

            # Process any failed actions that were saved
            recovery_results = self.error_recovery.process_failed_actions()
            logger.info(f"Failed action recovery results: {recovery_results}")

            # Log successful completion
            self.audit_logger.log_event(
                event_type="gold_tier_cycle_complete",
                description="Completed Gold Tier processing cycle",
                actor="orchestrator",
                result="success",
                parameters=results
            )

            logger.info(f"Gold Tier cycle completed with results: {results}")

        except Exception as e:
            error_id = self.error_recovery.log_error(
                e, "Error in Gold Tier processing cycle", "critical"
            )

            self.audit_logger.log_event(
                event_type="gold_tier_cycle_error",
                description=f"Error in Gold Tier processing cycle: {error_id}",
                actor="orchestrator",
                result="failed",
                parameters={"error_id": error_id}
            )

            raise e

        return results

def main():
    """Main function to demonstrate Gold Tier orchestrator"""
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure
    (vault_path / "Needs_Action").mkdir(exist_ok=True)
    (vault_path / "Done").mkdir(exist_ok=True)
    (vault_path / "Plans").mkdir(exist_ok=True)

    # Create a sample action file to process
    sample_action = vault_path / "Needs_Action" / "gold_tier_sample_action.md"
    sample_action.write_text("""---
type: gold_tier_test
priority: high
status: pending
created: 2026-02-19T12:40:00
---

# Gold Tier Test Action

This is a test action to verify all Gold Tier features are working.

## Requirements
- Process with audit logging
- Handle error recovery
- Demonstrate cross-domain integration
- Create appropriate plans
- Move to Done when complete

## Content
This action should trigger all Gold Tier features including Ralph Wiggum loops, audit logging, error recovery, and cross-domain integration.

## Expected Behavior
1. The action should be processed with full audit logging
2. Any errors should be handled gracefully
3. The file should be moved to the Done folder
4. All Gold Tier features should be demonstrated
""")

    orchestrator = GoldTierOrchestrator(str(vault_path))

    print("Running complete Gold Tier processing cycle...")
    results = orchestrator.run_complete_gold_tier_cycle()
    print(f"Gold Tier cycle results: {results}")

    print("\nDemonstrating Ralph Wiggum loop...")
    ralph_result = orchestrator.process_with_ralph_wiggum_loop(
        "Process any remaining files in Needs_Action folder",
        "gold_tier_test"
    )
    print(f"Ralph Wiggum loop result: {ralph_result}")

    print("\nChecking system health...")
    health_result = orchestrator.perform_system_health_check()
    print(f"System health: {health_result['overall_status']}")

    print("\nGold Tier Orchestrator demo completed!")

if __name__ == "__main__":
    main()