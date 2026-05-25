# Enrichment notes: Designing with Claude: From prompt to production

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 2
Pages fetched: 2/2

---

## Claude Code

**Current status:** Claude Code is a generally available AI-powered coding assistant deployable across terminal CLI, VS Code, JetBrains, desktop app, web, and other surfaces, requiring a Claude subscription or Anthropic Console account.

**Changes since talk:** The talk describes Claude Code primarily as a terminal/CLI tool that made engineers "really, really fast." Since then, Claude Code has expanded significantly: it now has a dedicated documentation site at code.claude.com, an Agent SDK, integrations with VS Code and JetBrains IDEs, a web interface, a desktop app, a Chrome extension (beta), computer use (preview), Slack integration, and remote control capability. The core CLI install method is now a single curl command (`curl -fsSL https://claude.ai/install.sh | bash`) with Homebrew and WinGet alternatives. Third-party provider support has been added for the terminal CLI and VS Code surfaces. These are expansions of scope, not contradictions of the talk's claims.

**Key details for chapter:**

- Claude Code installs via `curl -fsSL https://claude.ai/install.sh | bash` (macOS/Linux/WSL) or via Homebrew/WinGet; requires Claude subscription or Console account.
- The tool now spans terminal, IDE plugins, web, desktop, and Slack, making it a platform rather than a single CLI tool -- the acceleration effect described in the talk applies across all these surfaces now.
- A dedicated documentation index is available at `https://code.claude.com/docs/llms.txt` for programmatic discovery of all Claude Code pages.

---

## MCP

**Current status:** The MCP documentation page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404 Not Found response.

**Changes since talk:** The page has moved or been restructured. Based on training data: MCP (Model Context Protocol) is an open protocol Anthropic introduced to standardize how applications provide context and tools to LLMs. The canonical documentation and specification have migrated to `modelcontextprotocol.io` (the independent spec site) and the Anthropic API docs have reorganized their agents-and-tools section. The talk does not appear to discuss MCP directly by name; it is listed as an entity to enrich but is not referenced in the summary, quotes, or key claims. Caveat: the 404 prevents authoritative confirmation of current doc structure or any feature changes since the talk.

**Key details for chapter:**

- MCP is an open protocol for connecting LLMs to external tools and data sources via a standardized server/client interface; Anthropic publishes the spec but the protocol is open to third-party implementations.
- Given the 404, the current canonical reference for MCP is `https://modelcontextprotocol.io` rather than the Anthropic API docs URL provided.
- The chapter should verify whether MCP is actually referenced in the talk content before including it; based on the available summary and quotes, it does not appear as a named concept in this talk.

---

## Improvement opportunities

- **Development loop diagram:** Flow chart showing the four-stage cycle described in the talk (user feedback collection, feature design via prototype, code shipping with Claude Code, feedback analysis) with approximate time targets at each stage. Should illustrate how a 24-hour turnaround compresses the traditional product cycle.

- **PRD vs. prototype comparison table:** Side-by-side table contrasting the traditional PRD-driven workflow (document written, handed to eng, ambiguity resolved in meetings, implementation diverges from intent) against the prototype-driven workflow (conversational prototype built in Claude, fed as context, concrete artifact reduces ambiguity). Columns: artifact type, time to produce, precision, iteration cost, team coordination required.

- **Code example -- Claude Code CLAUDE.md configuration:** A sample `.claude/CLAUDE.md` file showing how a small product team like the one described would encode project context, conventions, and shorthand instructions so that all team members (engineers, PMs writing code, designers doing data) get consistent Claude Code behavior without coordination overhead.

- **Code example -- MCP server tool definition:** A minimal MCP server config in JSON showing a tool definition with `name`, `description`, and `inputSchema` fields, illustrating how the team could have built the internal tooling described ("built in an afternoon") by exposing a custom data source or feedback pipeline as an MCP tool accessible from Claude Code.

- **Worked example -- prototype-to-feature pipeline:** End-to-end walkthrough starting from a user complaint (per the "please complain at me" methodology), showing: the conversational Claude session that produces a prototype, the prototype artifact fed back as context, the Claude Code invocation that ships the feature, and the feedback loop check the next day. Concrete enough to be reproducible.

- **Timeline figure:** A horizontal timeline showing the ten-week build-to-launch arc, with labeled milestones (first prototype, first user session, internal tooling built, launch Friday, 62 improvements by Monday). Annotates where each methodology principle (dissolved roles, no PRDs, model improvements over engineering workarounds) was applied.

- **Comparison table -- team model tradeoffs:** Three-column table comparing large specialized team, small specialized team, and small dissolved-role team (the described approach) across: iteration cycle time, coordination overhead, tool-writing latency, feedback integration speed, and dependency on model quality. Makes explicit why the methodology requires model reliability as a prerequisite.
