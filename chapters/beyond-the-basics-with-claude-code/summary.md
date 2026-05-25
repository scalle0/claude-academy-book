# Summary: Beyond the basics with Claude Code

Chapter slug: `beyond-the-basics-with-claude-code`

## Abstract

This talk examines advanced customization strategies for Claude Code in large-scale software engineering environments. The speaker, an engineer on the Claude Code team, presents the thesis that effective agentic software engineering requires giving Claude access to everything a human developer can access, including team chat, CI/CD systems, internal documentation, and stakeholder communications. The talk explores three core customization needs: access to information sources beyond source code, knowledge of codebase conventions and institutional memory, and tooling that scales with model intelligence rather than compensating for lack thereof. A key focus is context window optimization, comparing it to constrained memory systems and highlighting the challenges of KV cache invalidation. The presentation analyzes four plugin primitives (MCP, skills, hooks, and agents) through the lens of scalability, examining what happens when monorepos contain tens of thousands of each primitive. The speaker advocates for zero-overhead abstractions and demonstrates advanced workflows using Git worktrees, persistent agents, agent teams, and automation features like slash loop for continuous monitoring of pull requests.

## Key claims

- If Claude cannot access everything a human developer can access, it cannot effectively perform software engineering tasks at scale
- Fine tuning is not cost efficient for customizing frontier models with company-specific information due to rapid model iteration
- The fastest way to improve agent performance is through tighter feedback loops rather than smarter models
- Context window sizes are remaining relatively constant while model capabilities improve, requiring better context engineering
- MCP servers do not scale well in large monorepos due to system prompt bloat from tool definitions
- Hooks provide true zero-overhead abstractions by running outside the context window and only injecting content when needed
- Professional software engineering work happens primarily outside source code in design documents, team communications, and stakeholder discussions
