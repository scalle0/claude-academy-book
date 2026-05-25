# Enrichment notes: Building signals that trade themselves

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 4
Pages fetched: 4/4

---

## Claude

**Current status:** The current flagship generally available model is Claude Opus 4.7, with the Claude 4 generation spanning Opus 4.7, Sonnet 4.6, and Haiku 4.5.

**Changes since talk:** The model lineup has advanced substantially. Claude 3.5 Sonnet and Claude 3.5 Haiku (which would have been current or recent at most plausible talk dates) are now legacy. The current generation is Claude 4, with Opus 4.7 as the top tier. Context windows on Opus and Sonnet are now 1M tokens. Pricing has shifted: Opus 4.7 is $5/MTok input, $25/MTok output; Sonnet 4.6 is $3/$15; Haiku 4.5 is $1/$5. Agentic coding is explicitly called out as a step-change improvement in Opus 4.7 over Opus 4.6, which is directly relevant to the autonomous signal generation described in the talk.

**Key details for chapter:**
- Current recommended model for complex agentic tasks is `claude-opus-4-7` (API ID), with 1M token context window and 128k max output.
- Claude 4 models are available via Claude API, AWS Bedrock, Vertex AI, and Microsoft Foundry; enterprise deployments like Man Group's have multiple deployment path options.
- Extended thinking is available on Sonnet 4.6 and Haiku 4.5 but not Opus 4.7; adaptive thinking is available on Opus 4.7 and Sonnet 4.6.

---

## Claude Code

**Current status:** Claude Code is a full-featured AI coding assistant available as a terminal CLI, VS Code extension, JetBrains IDE plugin, desktop app, and web interface.

**Changes since talk:** Claude Code has expanded significantly beyond a terminal tool. It now includes a web interface, desktop app, Chrome extension (beta), computer use (preview), Slack integration, and remote control capabilities. The Agent SDK is now a documented surface. Hooks for automation, scheduled prompt runs, and external event pushing are all present. The sidebar navigation shows "Agent SDK" and "What's New" as top-level sections, indicating ongoing rapid development.

**Key details for chapter:**
- Claude Code supports multi-surface deployment: terminal, IDE plugins, web, and desktop, making it viable for enterprise rollout to 750 non-engineer users across departments.
- The tool supports subagents, agent teams, and parallel work via worktrees, which maps directly to the "swarms of agents" vision described at the end of the talk.
- Installation is via `curl -fsSL https://claude.ai/install.sh | bash` on macOS/Linux/WSL, or via Homebrew/WinGet; third-party provider support is available for organizations with specific procurement constraints.

---

## MCP

**Current status:** The page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404 Not Found.

**Changes since talk:** The MCP documentation has moved. Based on training data and the Claude Code docs sidebar (which lists "Model Context Protocol (MCP)" under "Tools and plugins" at `https://code.claude.com/docs/`), MCP documentation now lives primarily within the Claude Code documentation rather than the main API docs. The MCP protocol itself has matured: it is now an open standard with a broad ecosystem of prebuilt plugins, and the Claude Code docs reference "Discover and install prebuilt plugins" and "Create plugins" as distinct surfaces. The canonical MCP reference should be checked at `https://code.claude.com/docs/mcp` or `https://modelcontextprotocol.io`.

**Key details for chapter:**
- The original URL `docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` is dead; cite MCP via the Claude Code docs or `modelcontextprotocol.io`.
- MCP is the underlying protocol by which skills connect Claude to external systems; in the Claude Code context, MCP servers expose tools that skills can invoke.
- Prebuilt plugins are now a first-class concept in Claude Code, which means enterprise deployments can source governed connectors rather than building all integrations from scratch.

---

## skills

**Current status:** Skills in Claude Code are defined by placing a `SKILL.md` file in `.claude/skills/<skill-name>/`, making the skill available as a slash command (`/skill-name`) that loads only when invoked.

**Changes since talk:** The skills feature has been formalized and documented. Notably, custom commands (previously at `.claude/commands/`) have been merged into skills: a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` are now equivalent and both create `/deploy`. The key architectural property is lazy loading: skill body content is not loaded into context until the skill is invoked, meaning large reference procedures have near-zero cost until needed. Skills are positioned explicitly as a solution for repeated instruction patterns and for procedures that have outgrown `CLAUDE.md`.

**Key details for chapter:**
- Skill files live at `.claude/skills/<name>/SKILL.md`; the slash command name derives from the directory name. Existing `.claude/commands/` files continue to work identically.
- Skills load lazily: content enters the context window only on invocation. This is architecturally significant for enterprise deployments with large institutional knowledge bases, because 100+ governed skills don't inflate every session's context.
- The docs frame skills as the solution when "a section of CLAUDE.md has grown into a procedure rather than a fact," which maps precisely to Man Group's use case of encoding institutional trading workflows.

---

## Improvement opportunities

- **Skill file structure, code example**: Show a minimal `SKILL.md` for a trading-domain workflow, such as a backtesting invocation skill at `.claude/skills/run-backtest/SKILL.md`, with a realistic header block (description, parameters, steps) that illustrates how institutional procedure gets encoded. This concretizes the abstract "connective layer" claim.

- **Skills governance lifecycle, diagram**: A flow chart showing the governance stages: proposal, process-owner review, testing, merge to shared repository, versioning, deprecation. This directly addresses the talk's central lesson that ungoverned skill creation by power users produces fragmented, localized optimizations. The diagram should contrast the "before" state (power user creates local skill, no review) with the "after" state (pull request, process owner sign-off, shared deployment).

- **Signal development pipeline, diagram**: An end-to-end architecture diagram showing how Claude agents move from research through backtesting to productionization, with skills as the connective layer at each stage. Nodes: data retrieval skill, backtest runner skill, strategy proposal generator, signal productionization step, production deployment gate. This visualizes the claim "AI came up with the idea, AI got the data, AI ran the backtest, AI then wrote up the strategy proposal, and AI productionized the signal."

- **Power user vs. process owner adoption failure, comparison table**: A two-column table contrasting outcomes when skills are built by power users alone versus when process owners are involved. Columns: skill scope (local vs. organizational), backtesting consistency (inconsistent vs. reproducible), lifecycle ownership (informal vs. assigned), reuse rate (low vs. high), auditability (none vs. version-controlled). This makes concrete the "people problem" framing from the talk.

- **Skill invocation in an agentic loop, code example**: A pseudocode or Claude Code session transcript showing an agent autonomously invoking `/run-backtest`, interpreting results, then invoking `/submit-strategy-proposal`, demonstrating how governed skills compose into autonomous workflows. Should include the slash-command invocation syntax and show how the lazy-load property keeps intermediate steps from bloating context.

- **Model selection for agentic trading workloads, comparison table**: A table comparing Claude Opus 4.7, Sonnet 4.6, and Haiku 4.5 on dimensions relevant to the Man Group use case: context window, max output, latency, extended thinking availability, and cost per MTok. This lets readers make an informed model choice for long-context backtesting versus high-frequency signal generation subtasks.

- **MCP server tool definition, code example**: A minimal MCP server config showing a tool definition for a financial data retrieval capability (e.g., `get_price_history` with ticker and date range parameters), illustrating how existing institutional data systems get exposed to Claude skills via MCP. Note that the canonical URL for MCP docs has moved from `docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` and the chapter should update this reference.
