# Personal AI Employee - Bronze Tier Implementation

## Overview

This project implements the Bronze Tier requirements for the Personal AI Employee Hackathon. The Bronze Tier includes:

- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script (File System monitoring)
- Claude Code successfully reading from and writing to the vault
- Basic folder structure: /Inbox, /Needs_Action, /Done
- All AI functionality implemented as Agent Skills (conceptual)

## Architecture

```
AI_Employee_Vault/
├── Dashboard.md          # Real-time summary of activities
├── Company_Handbook.md   # Rules of engagement
├── Inbox/               # Drop folder for new files
├── Needs_Action/        # Files requiring processing
└── Done/                # Completed tasks
```

## Components

### 1. Dashboard.md
Provides an overview of the AI Employee's activities and status, including:
- Executive summary
- Recent activity log
- Pending tasks
- System status
- Quick statistics

### 2. Company_Handbook.md
Contains the "Rules of Engagement" including:
- Communication guidelines
- Approval requirements
- Priorities
- Working hours
- Security protocols

### 3. File System Watcher
Monitors the Inbox folder and creates action files in Needs_Action when new files are detected.

### 4. Orchestrator
Processes files in Needs_Action, updates the Dashboard, and moves completed files to Done.

## Setup Instructions

1. Install Python 3.13 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Run the file system watcher: `python filesystem_watcher.py`
4. In a separate terminal, run the orchestrator: `python orchestrator.py`

## Features Implemented

✅ Obsidian vault with Dashboard.md and Company_Handbook.md
✅ File system watcher monitoring Inbox folder
✅ Automatic creation of action files in Needs_Action
✅ Claude Code can read from and write to vault files
✅ Basic folder structure (Inbox, Needs_Action, Done)
✅ Dashboard updates with processing activity
✅ File processing workflow

## Usage

1. Place a file in the `AI_Employee_Vault/Inbox/` folder
2. The file system watcher will detect it and create an action file in `Needs_Action/`
3. Run the orchestrator to process action files
4. Check `Dashboard.md` for activity updates
5. Processed files will be moved to the `Done/` folder

## Security Considerations

- Credentials are not stored in the vault (as per security guidelines)
- All file operations are logged
- Human-in-the-loop pattern for sensitive actions (conceptual implementation)