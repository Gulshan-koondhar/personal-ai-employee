# Tier Organization Summary

This document explains how files have been organized into bronze, silver, and gold tiers based on the Personal AI Employee Hackathon requirements.

## Bronze Tier
The bronze tier contains the foundational components of the AI employee system:

- **AI_Employee_Vault/**: The Obsidian vault with Dashboard.md and Company_Handbook.md
- **filesystem_watcher.py**: Monitors the /Inbox folder for new files
- **orchestrator.py**: Processes files in /Needs_Action and updates the dashboard
- **BRONZE_TIER_COMPLETED.md**: Documentation of completed bronze tier requirements

These components implement the basic requirements: vault with dashboard, file system watcher, orchestrator, folder structure (/Inbox, /Needs_Action, /Done), and agent skills.

## Silver Tier
The silver tier builds upon bronze with enhanced functionality:

- **linkedin_poster.py**: LinkedIn posting functionality
- **watcher_manager.py**: Manages multiple watcher scripts concurrently
- **schedule_manager.py**: Time-based task scheduling
- **mcp_config.json**: MCP server configuration
- **delete_linkedin_post.py**, **get_linkedin_urn.py**, **get_linkedin_urn_v2.py**, **test_linkedin_post.py**, **test_linkedin_post_v2.py**: LinkedIn integration utilities
- **watchers/**: Directory for various watcher implementations
- **SILVER_TIER_COMPLETED.md**: Documentation of completed silver tier requirements

These components implement silver tier requirements: multiple watcher scripts, LinkedIn posting, Claude reasoning loop with Plan.md, MCP server, human-in-the-loop approval workflow, and scheduling.

## Gold Tier
The gold tier includes all advanced features and integrations:

- **cross_domain_integration.py**: Cross-domain integration between personal and business domains
- **twitter_integration.py**: Twitter (X) integration
- **social_integration.py**: Facebook and Instagram integration
- **ceo_briefing_generator.py**: Weekly audit and CEO briefing system
- **audit_logger.py**: Comprehensive audit logging system
- **error_recovery.py**: Error handling and graceful degradation
- **gold_tier_orchestrator.py**: Main orchestrator for gold tier features
- **ralph_wiggum_loop.py**: Persistent task completion loops
- **GOLD_TIER_COMPLETED.md**: Documentation of completed gold tier requirements
- **agent_skills/**: Enhanced agent skills from previous tiers with gold tier capabilities
- **mcp_servers/**: Enhanced MCP servers including odoo-mcp.js for accounting integration
- Configuration files: .env, .gitignore, config_loader.py, package.json, requirements.txt
- Documentation files: CONFIGURATION.md, README.md

These components implement gold tier requirements: cross-domain integration, accounting system integration (Odoo), social media integrations, multiple MCP servers, weekly audits, error recovery, and comprehensive logging.

## Notes
- Some directories like `agent_skills` and `mcp_servers` are present in both silver and gold tiers because they contain components relevant to both tiers.
- The gold tier contains the most comprehensive implementation with all features from previous tiers plus all gold tier enhancements.