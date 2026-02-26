"""
Cleanup script for social media approval files
Removes old test approvals and keeps only the project status post
"""
import os
from pathlib import Path
import shutil

# Paths
script_dir = Path(__file__).parent.absolute()
vault_path = script_dir / "AI_Employee_Vault"
pending_dir = vault_path / "Plans" / "Pending_Approval" / "Social_Media"
approved_dir = vault_path / "Plans" / "Approved" / "Social_Media"
rejected_dir = vault_path / "Plans" / "Rejected" / "Social_Media"
published_dir = vault_path / "Social_Posts" / "Published"
social_posts_dir = vault_path / "Social_Posts"

print("="*60)
print("SOCIAL MEDIA APPROVAL CLEANUP")
print("="*60)

# Files to keep
keep_files = [
    "SOCIAL_APPROVAL_LINKEDIN_PROJECT_STATUS_20260226.md",
    "LINKEDIN_PROJECT_STATUS_20260226.md"
]

# Cleanup Pending Approvals
print("\n[PENDING] Cleaning Pending Approvals...")
if pending_dir.exists():
    for file in pending_dir.glob("*.md"):
        if file.name not in keep_files:
            file.unlink()
            print(f"  [DELETE] {file.name}")
        else:
            print(f"  [KEEP]   {file.name}")
    
    remaining = list(pending_dir.glob("*.md"))
    print(f"  Result: {len(remaining)} file(s) remaining")

# Cleanup Approved (except project status)
print("\n[APPROVED] Cleaning Approved...")
if approved_dir.exists():
    for file in approved_dir.glob("*.md"):
        if "PROJECT_STATUS" not in file.name:
            file.unlink()
            print(f"  [DELETE] {file.name}")
        else:
            print(f"  [KEEP]   {file.name}")
    
    remaining = list(approved_dir.glob("*.md"))
    print(f"  Result: {len(remaining)} file(s) remaining")

# Cleanup Rejected
print("\n[REJECTED] Cleaning Rejected...")
if rejected_dir.exists():
    count = 0
    for file in rejected_dir.glob("*.md"):
        file.unlink()
        count += 1
        print(f"  [DELETE] {file.name}")
    print(f"  Result: {count} file(s) deleted")

# Cleanup Published (old test posts)
print("\n[PUBLISHED] Cleaning Published...")
if published_dir.exists():
    for file in published_dir.glob("*.md"):
        if "PROJECT_STATUS" not in file.name:
            file.unlink()
            print(f"  [DELETE] {file.name}")
    
    remaining = list(published_dir.glob("*.md"))
    print(f"  Result: {len(remaining)} file(s) remaining")

# Cleanup old draft posts (keep project status)
print("\n[SOCIAL POSTS] Cleaning old drafts...")
if social_posts_dir.exists():
    for file in social_posts_dir.glob("*.md"):
        if file.name.startswith(".") or file.name == "APPROVAL_DASHBOARD.md":
            continue
        if "PROJECT_STATUS" not in file.name:
            file.unlink()
            print(f"  [DELETE] {file.name}")
    
    remaining = [f for f in social_posts_dir.glob("*.md") if not f.name.startswith(".")]
    print(f"  Result: {len(remaining)} file(s) remaining")

print("\n" + "="*60)
print("CLEANUP COMPLETE")
print("="*60)
print("\nReady to publish:")
print("  LINKEDIN_PROJECT_STATUS_20260226.md")
print("\nApproval file location:")
print(f"  {pending_dir / 'SOCIAL_APPROVAL_LINKEDIN_PROJECT_STATUS_20260226.md'}")
print("="*60)
