# Personal AI Employee - Run Guide

Complete guide to running Bronze, Silver, and Gold tiers of the Personal AI Employee.

---

## 📋 Prerequisites (All Tiers)

### 1. Install Python 3.13+
```bash
python --version  # Should be 3.13 or higher
```

### 2. Install Node.js (for MCP servers)
```bash
node --version  # Should be v24+ LTS
npm --version
```

### 3. Install Python Dependencies
```bash
# Navigate to project root
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant"

# Install dependencies
pip install -r gold/requirements.txt
```

### 4. Install Node.js Dependencies (for MCP servers)
```bash
cd gold/mcp_servers
npm install
```

### 5. Configure Environment Variables
Edit the `.env` file in the `gold` folder with your actual credentials:
```bash
# Open .env file
# Replace placeholder values with real credentials
```

---

## 🥉 Bronze Tier

### What It Does
- Monitors `/Inbox` folder for new files
- Creates action files in `/Needs_Action`
- Processes files and updates `Dashboard.md`
- Moves completed files to `/Done`

### How to Run

**Step 1: Start the File System Watcher**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/bronze"
python filesystem_watcher.py
```

**Step 2: Run the Orchestrator (separate terminal)**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/bronze"
python orchestrator.py
```

### Usage
1. Place any file in `AI_Employee_Vault/Inbox/`
2. Watcher detects the file and creates an action file in `Needs_Action/`
3. Orchestrator processes the action file
4. Check `AI_Employee_Vault/Dashboard.md` for updates
5. Processed files move to `AI_Employee_Vault/Done/`

### Stop
Press `Ctrl+C` in both terminal windows to stop the watcher and orchestrator.

---

## 🥈 Silver Tier

### What It Does
All Bronze features PLUS:
- Gmail, WhatsApp, LinkedIn watchers
- LinkedIn auto-posting
- Scheduled tasks (daily briefing, weekly audit)
- MCP server for email
- Human-in-the-loop approval workflow
- Plan.md creation

### How to Run

**Step 1: Install Dependencies**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/silver"
pip install -r ../gold/requirements.txt
```

**Step 2: Start Multiple Watchers (Watcher Manager)**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/silver"
python watcher_manager.py
```

**Step 3: Start Schedule Manager (separate terminal)**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/silver"
python schedule_manager.py
```

**Step 4: Run LinkedIn Poster (optional, for testing)**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/silver"
python test_linkedin_post.py
```

**Step 5: Start MCP Email Server (separate terminal)**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold/mcp_servers"
node email-mcp.js
```

### Scheduled Tasks
- **Daily Briefing**: Runs every day at 8:00 AM
- **Weekly Audit**: Runs every Monday at 9:00 AM
- **LinkedIn Post**: Runs Tuesday & Thursday at 12:00 PM

### Usage
1. Configure your Gmail, LinkedIn credentials in `.env`
2. Start watcher_manager.py to monitor all platforms
3. Check `AI_Employee_Vault/Needs_Action/` for new action items
4. Approve sensitive actions by moving files from `Pending_Approval/` to `Approved/`

---

## 🥇 Gold Tier

### What It Does
All Silver features PLUS:
- Cross-domain integration (Personal + Business)
- Odoo accounting integration
- Facebook & Instagram integration
- Twitter (X) integration
- Weekly CEO Briefing generation
- Error recovery & graceful degradation
- Comprehensive audit logging
- Ralph Wiggum autonomous loops

### How to Run

**Step 1: Configure Environment Variables**
```bash
# Edit the .env file with ALL your credentials
# Email, Odoo, Twitter, Facebook, Instagram, LinkedIn, Gmail, WhatsApp
```

**Step 2: Start MCP Servers (separate terminals)**

**Email MCP Server:**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold/mcp_servers"
node email-mcp.js
```

**Odoo MCP Server:**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold/mcp_servers"
node odoo-mcp.js
```

**Step 3: Start Gold Tier Orchestrator**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python gold_tier_orchestrator.py
```

**Step 4: Start Individual Components (optional, separate terminals)**

**Cross-Domain Integration:**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python cross_domain_integration.py
```

**CEO Briefing Generator:**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python ceo_briefing_generator.py
```

**Social Media Integration:**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python social_integration.py
```

**Twitter Integration:**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python twitter_integration.py
```

**Audit Logger (runs automatically with other components)**
```bash
# No need to run separately - integrated into all Gold tier components
```

**Error Recovery (runs automatically with other components)**
```bash
# No need to run separately - integrated into all Gold tier components
```

**Ralph Wiggum Loop (for autonomous task completion):**
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python ralph_wiggum_loop.py
```

### Usage

#### Generate Weekly CEO Briefing
```bash
cd "/mnt/e/Gulshan/Quarter 4 Hackathon/personal_AI_assistant/gold"
python ceo_briefing_generator.py
# Check AI_Employee_Vault/Briefings/ for generated briefing
```

#### Post to Social Media
- Posts are created as drafts in `AI_Employee_Vault/Social_Posts/`
- Review and approve before publishing
- Or use the automated scheduling

#### Cross-Domain Events
- Automatically detects personal/business overlap
- Creates integration files in `AI_Employee_Vault/Integration/`

#### Audit Logs
- Check `AI_Employee_Vault/Logs/` for:
  - `audit_log_YYYYMMDD.jsonl` - All activities
  - `error_log_YYYYMMDD.jsonl` - Error tracking

---

## 🏆 All Tiers - Quick Start Commands

### Bronze Tier (3 terminals)
```bash
# Terminal 1 - Watcher
cd bronze && python filesystem_watcher.py

# Terminal 2 - Orchestrator
cd bronze && python orchestrator.py
```

### Silver Tier (3+ terminals)
```bash
# Terminal 1 - Watcher Manager
cd silver && python watcher_manager.py

# Terminal 2 - Schedule Manager
cd silver && python schedule_manager.py

# Terminal 3 - MCP Server
cd gold/mcp_servers && node email-mcp.js
```

### Gold Tier (5+ terminals)
```bash
# Terminal 1 - MCP Email Server
cd gold/mcp_servers && node email-mcp.js

# Terminal 2 - MCP Odoo Server
cd gold/mcp_servers && node odoo-mcp.js

# Terminal 3 - Gold Orchestrator
cd gold && python gold_tier_orchestrator.py

# Terminal 4 - Ralph Wiggum Loop (optional)
cd gold && python ralph_wiggum_loop.py

# Terminal 5 - Schedule Manager
cd silver && python schedule_manager.py
```

---

## 🔧 Testing Your Setup

### Test Configuration
```bash
cd gold
python config_loader.py
```

### Test LinkedIn Posting
```bash
cd silver
python test_linkedin_post.py
```

### Test LinkedIn URN Retrieval
```bash
cd silver
python get_linkedin_urn_v2.py
```

---

## 📁 Directory Structure

```
personal_AI_assistant/
├── AI_Employee_Vault/       # Obsidian vault (shared by all tiers)
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Done/
│   ├── Plans/
│   ├── Briefings/
│   ├── Reports/
│   ├── Logs/
│   ├── Social_Posts/
│   └── LinkedIn_Posts/
│
├── bronze/                  # Bronze Tier
│   ├── filesystem_watcher.py
│   └── orchestrator.py
│
├── silver/                  # Silver Tier
│   ├── watcher_manager.py
│   ├── schedule_manager.py
│   ├── linkedin_poster.py
│   └── watchers/
│
└── gold/                    # Gold Tier
    ├── gold_tier_orchestrator.py
    ├── cross_domain_integration.py
    ├── twitter_integration.py
    ├── social_integration.py
    ├── ceo_briefing_generator.py
    ├── audit_logger.py
    ├── error_recovery.py
    ├── ralph_wiggum_loop.py
    ├── config_loader.py
    ├── mcp_servers/
    │   ├── email-mcp.js
    │   └── odoo-mcp.js
    └── agent_skills/
```

---

## ⚠️ Important Notes

1. **Always start watchers before orchestrator** - Watchers create action files that orchestrator processes

2. **Keep terminals open** - Watchers and orchestrators run continuously

3. **Check logs** - All components log to console and files in `AI_Employee_Vault/Logs/`

4. **Credentials** - Make sure `.env` has valid credentials for services you want to use

5. **Approval Workflow** - Sensitive actions require moving files from `Pending_Approval/` to `Approved/`

6. **Stop gracefully** - Use `Ctrl+C` to stop all running processes

---

## 🐛 Troubleshooting

### Watcher not detecting files
- Ensure the Inbox folder path is correct
- Check watcher.log for errors
- Verify file permissions

### MCP Server not starting
- Install Node.js dependencies: `npm install`
- Check Node.js version (should be v24+)

### API errors
- Verify credentials in `.env`
- Check API key permissions
- Test API connectivity manually

### Python import errors
- Install dependencies: `pip install -r gold/requirements.txt`
- Ensure Python 3.13+

---

**For more details, see:**
- `gold/CONFIGURATION.md` - Configuration guide
- `gold/README.md` - Project overview
- `GOLD_TIER_COMPLETED.md` - Gold tier features
- `SILVER_TIER_COMPLETED.md` - Silver tier features
- `BRONZE_TIER_COMPLETED.md` - Bronze tier features
