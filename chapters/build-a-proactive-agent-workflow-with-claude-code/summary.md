# Summary: Build a proactive agent workflow with Claude Code

Chapter slug: `build-a-proactive-agent-workflow-with-claude-code`

## Abstract

This talk introduces Routines, a new feature in Claude Code that enables proactive agent workflows without requiring users to manage infrastructure. The presentation addresses three key challenges in building proactive agents: deployment complexity, trigger management, and human-in-the-loop interactions. Routines allows users to define automated Claude Code sessions through prompts, repository connections, connectors, and triggers, with all hosting and session management handled by Claude Code's infrastructure. The feature supports both time-based and event-based triggers, including native GitHub events and custom webhooks. The speaker demonstrates two practical examples: automated documentation creation triggered weekly and issue-based documentation updates triggered by GitHub events. Sessions remain interactive and steerable through web, CLI, and desktop interfaces, allowing real-time monitoring and intervention. The talk emphasizes moving from reactive tools to proactive teammates, where agents can autonomously detect problems and take action without waiting for user input.

## Key claims

- Routines eliminates infrastructure management burden by running on Claude Code's managed infrastructure with automatic hosting, session state, and connector authentication
- Proactive agents that respond to events and schedules are superior to reactive agents that wait for manual triggers
- Time-based and event-based triggers enable comprehensive automation workflows, including native GitHub event integration
- Interactive sessions allow real-time steering and monitoring of automated routines through multiple interfaces
- Multi-agent patterns like generator-critiquer can be implemented using multiple coordinated routines
- Context provision through repository access and connector integrations determines the ceiling of agent success
- Weekly PRs for Claude Code have increased 200% since the beginning of the year, creating documentation maintenance challenges
