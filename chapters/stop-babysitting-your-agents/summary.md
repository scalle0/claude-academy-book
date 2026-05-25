# Summary: Stop babysitting your agents

Chapter slug: `stop-babysitting-your-agents`

## Abstract

This talk presents strategies for reducing manual supervision of AI agents by implementing automated verification loops, parallel processing, and background automation. The speaker argues that current software development involves excessive monitoring of Claude's work, which is inefficient. The proposed solution centers on three core concepts: verification (teaching Claude to check its own work through automated testing loops), multi-clauding (running multiple Claude instances in parallel with better session management), and background loops (using scheduled routines to handle repetitive tasks). The verification approach involves giving Claude access to tools for building, testing, and validating code changes, similar to human development workflows but automated. Multi-clauding utilizes features like Claude Code desktop app, agent view, and remote control to manage multiple concurrent sessions. Background loops employ scheduled prompts and routines to handle maintenance tasks like PR management and documentation updates without human intervention. The talk emphasizes that agents need similar verification tools as humans but require explicit access to these capabilities through proper tooling and instruction configuration.

## Key claims

- Most software tooling was built for humans but needs adaptation for AI agents to work effectively
- Verification loops allow Claude to autonomously debug and improve code by giving it tools to check its own work
- Skills can be made self-improving by instructing them to document and update themselves when encountering blockers
- Human attention becomes the bottleneck when managing more than four to five Claude sessions simultaneously
- Background loops and routines can handle repetitive development tasks like PR management without human intervention
- Remote control functionality allows managing Claude sessions from mobile devices through notifications
- The same verification strategies humans use for software development can be effectively applied to agent workflows
