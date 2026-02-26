---
type: test_file
priority: high
status: pending
created: 2026-02-26T10:00:00
---

# Bronze Tier Test 1: File System Watcher

## Test Objective
Verify that the file system watcher detects new files in the Inbox folder and creates action files in Needs_Action.

## Test Steps
1. Place this file in the Inbox folder
2. File system watcher should detect it
3. Action file should be created in Needs_Action
4. Original file should be moved with .original extension

## Expected Result
- Action file created in Needs_Action folder
- Original file moved with .original extension

## Test Status
- [ ] File placed in Inbox
- [ ] Watcher detected file
- [ ] Action file created
- [ ] Original file moved
- [ ] Test PASSED
