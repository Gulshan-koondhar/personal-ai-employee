"""
Ralph Wiggum Loop for AI Employee

Implements the persistence pattern that keeps the AI working autonomously
until a task is complete by using a Stop hook that intercepts Claude's exit
and feeds the prompt back.
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RalphWiggumLoop:
    """Implements the Ralph Wiggum persistence pattern for autonomous task completion"""

    def __init__(self, vault_path: str, max_iterations: int = 10):
        self.vault_path = Path(vault_path)
        self.max_iterations = max_iterations
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.logs = self.vault_path / "Logs"

        # Create necessary directories
        self.logs.mkdir(parents=True, exist_ok=True)

    def check_completion_by_file_movement(self, task_identifier: str = None) -> bool:
        """
        Check if task is complete by looking for file movement to Done folder.
        This is the advanced Gold-tier completion strategy.
        """
        # Check if specific task files have moved to Done
        if task_identifier:
            # Look for files related to the specific task in Done folder
            for done_file in self.done.glob(f"*{task_identifier}*"):
                return True

        # Check if Needs_Action is empty (basic completion check)
        action_files = list(self.needs_action.glob("*.md"))
        needs_action_count = len([f for f in action_files if not f.name.startswith('.')])

        return needs_action_count == 0

    def check_completion_by_promise(self, output: str) -> bool:
        """
        Check if task is complete by looking for completion promise in output.
        """
        return "<promise>TASK_COMPLETE</promise>" in output

    def run_loop(self, initial_prompt: str, task_identifier: str = None):
        """
        Run the Ralph Wiggum loop until task is complete or max iterations reached.
        """
        logger.info(f"Starting Ralph Wiggum loop for task: {task_identifier or 'Unknown'}")
        logger.info(f"Max iterations: {self.max_iterations}")

        iteration = 0
        current_prompt = initial_prompt

        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}: Processing task")

            # Log the current state
            needs_action_count = len(list(self.needs_action.glob("*.md")))
            logger.info(f"Files in Needs_Action: {needs_action_count}")

            # Check if task is complete (file movement strategy - Gold tier)
            if self.check_completion_by_file_movement(task_identifier):
                logger.info(f"Task completed! All files moved to Done folder.")
                return {"status": "completed", "iterations": iteration, "reason": "file_movement_complete"}

            # Here we would normally call Claude Code with the prompt
            # For simulation, we'll just process the existing files
            result = self.simulate_claude_processing(current_prompt, iteration)

            # Check if task is complete by promise (alternative strategy)
            if self.check_completion_by_promise(result.get("output", "")):
                logger.info(f"Task completed! Completion promise found.")
                return {"status": "completed", "iterations": iteration, "reason": "promise_complete"}

            # If we're at max iterations without completion
            if iteration >= self.max_iterations:
                logger.warning(f"Max iterations ({self.max_iterations}) reached without task completion")
                return {"status": "max_iterations_reached", "iterations": iteration, "reason": "max_iterations_reached"}

            # Prepare for next iteration with updated prompt
            current_prompt = self.prepare_next_iteration_prompt(current_prompt, result, iteration)

        logger.info("Ralph Wiggum loop completed")
        return {"status": "completed", "iterations": iteration}

    def simulate_claude_processing(self, prompt: str, iteration: int):
        """
        Simulate Claude processing of the prompt.
        In real implementation, this would call Claude Code API.
        """
        logger.info(f"Simulating Claude processing for iteration {iteration}")

        # Process any files in Needs_Action
        action_files = list(self.needs_action.glob("*.md"))

        processed_files = []
        for action_file in action_files:
            if action_file.name.startswith('.'):
                continue  # Skip hidden files

            # Read and process the action file
            content = action_file.read_text()

            # Update content to mark as processed in this iteration
            updated_content = content + f"\n\n## Processing Log\n- [x] Processed in iteration {iteration} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n- [ ] Moved to Done folder\n- [ ] Task complete"

            # Write updated content back
            action_file.write_text(updated_content)

            # Move to Done folder (this would trigger completion in Gold tier)
            done_file = self.done / action_file.name

            # Handle case where file already exists in Done folder
            if done_file.exists():
                # Add timestamp to make unique
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                done_file = self.done / f"{action_file.stem}_{timestamp}{action_file.suffix}"

            action_file.rename(done_file)

            processed_files.append(str(done_file))
            logger.info(f"Moved {action_file.name} to Done folder as {done_file.name}")

        return {
            "output": f"Processed {len(processed_files)} files in iteration {iteration}",
            "processed_files": processed_files,
            "needs_action_remaining": len(list(self.needs_action.glob("*.md")))
        }

    def prepare_next_iteration_prompt(self, current_prompt: str, result: dict, iteration: int):
        """
        Prepare the prompt for the next iteration based on current results.
        """
        # In a real implementation, this would analyze Claude's output
        # and prepare a new prompt with updated context
        return f"{current_prompt}\n\nIteration {iteration} completed. Result: {result.get('output', 'Unknown')}. Continue processing remaining tasks."

    def create_task_monitoring_file(self, task_description: str, task_id: str = None):
        """
        Create a state file that tracks the progress of a specific task.
        """
        if not task_id:
            task_id = f"task_{int(time.time())}"

        state_file = self.logs / f"ralph_loop_state_{task_id}.json"

        state_data = {
            "task_id": task_id,
            "description": task_description,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "iteration_count": 0,
            "max_iterations": self.max_iterations,
            "progress_log": []
        }

        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)

        logger.info(f"Created task monitoring file: {state_file.name}")
        return state_file

def main():
    """Main function to demonstrate Ralph Wiggum loop functionality"""
    vault_path = Path("../AI_Employee_Vault")

    # Create vault structure if needed
    (vault_path / "Needs_Action").mkdir(exist_ok=True)
    (vault_path / "Done").mkdir(exist_ok=True)

    # Create a test action file to process
    test_action = vault_path / "Needs_Action" / "test_autonomous_task.md"
    test_action.write_text("""---
type: test_task
priority: high
status: pending
created: 2026-02-19T12:35:00
---

# Test Autonomous Task

This is a test task to verify the Ralph Wiggum loop functionality.

## Task Details
- Process this file autonomously
- Move it to Done when complete
- Demonstrate persistence pattern

## Steps
- [ ] Review the task requirements
- [ ] Process the content
- [ ] Update status
- [ ] Move to Done folder

## Expected Outcome
The file should be moved to the Done folder through autonomous processing.
""")

    # Create the Ralph Wiggum loop
    ralph_loop = RalphWiggumLoop(str(vault_path), max_iterations=5)

    # Create a task monitoring file
    state_file = ralph_loop.create_task_monitoring_file(
        "Test autonomous task processing with Ralph Wiggum loop",
        "test_autonomous_1"
    )

    # Run the loop
    result = ralph_loop.run_loop(
        "Process all files in Needs_Action, move to Done when complete",
        task_identifier="test_autonomous"
    )

    logger.info(f"Ralph Wiggum loop completed with result: {result}")

    # Update the state file with completion status
    if state_file.exists():
        with open(state_file, 'r') as f:
            state_data = json.load(f)

        state_data.update({
            "status": "completed",
            "final_result": result,
            "completed_at": datetime.now().isoformat()
        })

        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)

    print(f"Ralph Wiggum loop completed: {result}")
    print(f"Check {vault_path}/Done/ to see the processed file.")

if __name__ == "__main__":
    main()