# Enrichment notes: From one person to 80: Scaling a hypergrowth engineering org with Claude Code

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 3/3

---

## Claude Code

**Current status:** Claude Code is a generally available AI-powered coding assistant that works across terminal, VS Code, JetBrains, desktop app, and web surfaces, installable via curl, Homebrew, or WinGet.

**Changes since talk:** The overview page shows Claude Code has expanded significantly in distribution and integration surface. The talk describes Claude Code primarily as a terminal/CLI tool used for agentic workflows. Current docs show additional surfaces including a desktop app, web interface, Chrome extension (beta), computer use (preview), Slack integration, and remote control. The install path has also been standardized to `curl -fsSL https://claude.ai/install.sh | bash`.

**Key details for chapter:**
- Claude Code supports third-party model providers in the Terminal CLI and VS Code surfaces, not just Anthropic's own models.
- The `.claude` directory is a first-class concept with documented structure for storing instructions, memories, skills, and hooks.
- Prompt caching is documented as a feature relevant to Claude Code sessions, which is directly relevant to the cost model when running repeated agentic workflows like the PR review and QA automation described in the talk.

---

## MCP

**Current status:** The MCP documentation page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404/Not Found response.

**Changes since talk:** The page failed to fetch. Based on training data: MCP (Model Context Protocol) is Anthropic's open protocol for connecting Claude to external tools and data sources via standardized server definitions. The talk references using an MCP (referred to as "post-hoc MCP" in the transcript quote) to connect historical AB testing data to Claude for generating experimentation guidelines. The current Claude Code docs sidebar shows MCP is now documented under the "Tools and plugins" section at `https://docs.anthropic.com/en/docs/claude-code/mcp` rather than the agents-and-tools path. The canonical MCP specification lives at `modelcontextprotocol.io`. Cannot confirm specific API changes without a successful fetch.

**Key details for chapter:**
- MCP in Claude Code is now surfaced under "Tools and plugins" in the Claude Code docs, with support for discovering and installing prebuilt plugins as well as creating custom ones.
- The talk's reference to "post-hoc MCP" likely means a custom MCP server wrapping a database of historical AB test records; this pattern (wrapping internal data stores as MCP servers) is the standard integration pattern.
- Caveat: specific current MCP tool definition schema and any breaking changes since the talk cannot be confirmed due to the fetch failure.

---

## Skills

**Current status:** Skills are reusable, on-demand instruction sets defined by a `SKILL.md` file in `.claude/skills/<name>/`, invocable via `/skill-name` in Claude Code chat.

**Changes since talk:** The skills page reveals a significant naming consolidation: custom commands (previously stored as `.claude/commands/<name>.md`) have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` are now equivalent. The talk describes "Claude Code skills" as the mechanism for QA automation combining browser automation with database setup tools; this maps directly to the current skills feature. The key behavioral characteristic noted in current docs is that a skill's body loads only when invoked, so long reference material has no context cost until needed, which is directly relevant to the QA use case described.

**Key details for chapter:**
- Skills are lazy-loaded: content is not in the context window until the skill is invoked, making them appropriate for large procedural references like multi-step QA scenarios.
- The `/skill-name` invocation syntax is explicit; Claude also invokes skills automatically when it judges them relevant without explicit user invocation.
- Built-in bundled skills include `/debug` and `/code-review`; the talk's automated PR review pattern could be implemented as a custom skill wrapping historical review patterns.

---

## Improvement opportunities

- **Onboarding prompt pair, worked example:** The talk describes two specific prompts given to every new engineer ("go over all commits and tell me what everyone can do"). The chapter would benefit from a concrete worked example showing the exact prompt structure, the `git log` command piped to Claude Code, and a sample output schema, illustrating the commit-history-as-org-map pattern end to end.

- **PR review skill definition, code example:** A `SKILL.md` file showing how to encode historical PR feedback patterns as a reusable skill, including the frontmatter fields, the instruction body referencing a `REVIEW_HISTORY.md` context file, and the `/pr-review` invocation, would make the automated code review claim concrete and actionable.

- **MCP server config, code example:** A minimal MCP server configuration (JSON tool definition + handler stub) showing how to wrap an internal AB test results database as an MCP tool, matching the "post-hoc MCP" pattern described in the talk. Should include the tool `name`, `description`, `inputSchema`, and a note on where the config file lives in the `.claude` directory.

- **Evaluation pipeline architecture, diagram:** A flow diagram showing the three-component evaluation pipeline described in the talk: user simulator (Claude generating synthetic user inputs), Stage Hand browser automation (executing against the live app), and the correctness assertion layer. Should distinguish this "behavioral correctness" approach from model-output evals and show data flow between components.

- **Frustration classification prompt, code example:** A concrete prompt template for classifying user chat messages into frustration levels (e.g., a 1-5 scale with per-level criteria), along with a note on how to pipe production conversation logs through it as a monitoring cron, illustrating the "user silence as success signal" insight.

- **Scaling phase comparison table:** A two-column table comparing the 1-15 engineer phase against the 50-80 engineer phase: problems encountered, tools/approaches applied, and complexity level of the solution. This directly maps to the talk's structure and makes the "simplicity scales" thesis scannable.

- **Skills vs. CLAUDE.md decision guide, comparison table:** A side-by-side table covering when to use a skill (`SKILL.md`) versus when to put instructions in `CLAUDE.md`, using the docs' own criteria (procedural vs. factual, always-loaded vs. on-demand, length considerations) applied to the specific use cases from the talk (QA automation, PR review, org mapping).
