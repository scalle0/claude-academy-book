# Enrichment notes: Beyond the basics with Claude Code

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 9
Pages fetched: 6/7

---

## Claude Code

**Current status:** Claude Code is a production AI coding assistant available as a CLI, VS Code extension, JetBrains plugin, desktop app, and web interface, supporting terminal, IDE, and browser workflows.

**Changes since talk:** The docs now show a substantially expanded surface area: web interface, desktop app, Chrome extension (beta), computer use (preview), Slack integration, and remote control. The documentation structure has been reorganized under a `code.claude.com` domain with its own dedicated docs site, separate from `docs.anthropic.com`. The sidebar reveals an "Agent SDK" section, suggesting programmatic agent construction has been formalized beyond what was described in the talk.

**Key details for chapter:**
- Installation via `curl -fsSL https://claude.ai/install.sh | bash` on macOS/Linux/WSL; WinGet on Windows; Homebrew available as an alternative.
- The docs now distinguish "Build with Claude Code," "Administration," "Configuration," "Reference," and "Agent SDK" as top-level sections, indicating the feature set has grown considerably since a talk describing it as a customization-focused tool.
- Third-party model provider support is noted for the Terminal CLI and VS Code extension, which the talk did not mention.

---

## KV Cache

**Current status:** Prompt caching on the Anthropic API supports both automatic caching (top-level `cache_control` field) and explicit cache breakpoints on individual content blocks, with 5-minute and 1-hour TTL options.

**Changes since talk:** Several significant additions since the talk:

- **Automatic caching** is a new mode where you add a single `cache_control` field at the request top level and the system moves the breakpoint forward automatically as conversations grow. This did not exist at the time of the talk, which assumed manual breakpoint placement.
- **1-hour cache duration** is now available at 2x the base input token price (`{"type": "ephemeral", "ttl": "1h"}`), up from the 5-minute default.
- **Cache diagnostics (beta)** appears as a new feature in the sidebar.
- The pricing table now covers Claude Opus 4.x and Sonnet 4.x model families. Claude Haiku 3.5 is retired on the main API (Bedrock and Vertex AI excepted).
- Cache read tokens remain at 0.1x base input price; write tokens at 1.25x (5-minute) or 2x (1-hour).

**Key details for chapter:**
- The talk's framing of KV cache as requiring careful manual placement is now partially superseded: automatic caching handles the common multi-turn conversation case without explicit breakpoints.
- The 5-minute default TTL and cache invalidation problem the speaker described remain accurate; the 1-hour option is now available for workloads where the 5-minute window is too short.
- Cache writes cost more than base input tokens (1.25x for 5-minute), which confirms the speaker's framing that you should distinguish "cheap tokens" (cache hits at 0.1x) from "expensive tokens" (fresh writes).

---

## MCP

**Current status:** The URL `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404; MCP documentation has moved.

The Claude Code docs sidebar shows MCP under "Tools and plugins" with entries for "Model Context Protocol (MCP)," "Discover and install prebuilt plugins," and "Create plugins." From training data: MCP is an open protocol for connecting Claude to external tools and data sources via standardized server definitions; tool schemas are injected into the system prompt, which is the scalability issue the speaker identified.

**Changes since talk:** The URL has moved; MCP is now documented under the Claude Code docs site rather than the main API docs. The sidebar shows a "prebuilt plugins" discovery mechanism, which suggests Anthropic has addressed some discoverability friction. The talk's core scalability critique (tool definitions bloating the system prompt in large monorepos) remains architecturally valid; no evidence from the fetched docs of a resolution to that issue.

**Key details for chapter:**
- MCP documentation has relocated; link to `https://code.claude.com/docs` and navigate to "Tools and plugins > Model Context Protocol."
- The plugin/MCP distinction in the current docs sidebar suggests "plugins" may be the preferred term for packaged MCP server bundles, while MCP refers to the underlying protocol.
- The talk's claim that MCP does not scale in large monorepos due to system prompt bloat from tool definitions remains the architectural reality; hooks and tool search are the documented mitigations.

---

## Agentic Loop

**Current status:** The Claude Code overview describes an agentic loop where Claude iterates through tool calls until a task is complete, with each tool call operating inside a context window.

**Changes since talk:** No significant changes to the core concept. The terminology is consistent with the talk. The docs now show more explicit tooling around the loop (hooks fire at `PreToolUse` and `PostToolUse` events, which are per-tool-call events within the loop), and the Agent SDK section suggests the loop is now more programmatically accessible.

**Key details for chapter:**
- The agentic loop is the execution model: Claude reasons, calls a tool, observes the result, reasons again, and repeats until done or stopped.
- Hook events `PreToolUse` and `PostToolUse` fire on every tool call inside the loop; `UserPromptSubmit` and `Stop` fire once per turn. This makes hooks the primary instrumentation point for the loop.
- Context window management within the loop is the central engineering challenge; subagents address this by running side tasks in separate context windows and returning only summaries.

---

## Git Worktrees

**Current status:** Git worktrees are documented under "Isolate sessions with worktrees" in the "Agents and parallel work" section of Claude Code docs.

**Changes since talk:** The feature has been promoted to a first-class documented workflow with its own page. At the time of the talk it was presented as an advanced technique the speaker's team used; it now has official documentation. The sidebar placement under "Agents and parallel work" alongside "Run agent teams" confirms worktrees are now framed as a parallelization primitive, not just an isolation trick.

**Key details for chapter:**
- Worktrees let multiple Claude Code sessions operate on the same repository simultaneously without conflicts, each in its own working directory.
- The canonical use case is parallel agent teams: one agent per worktree, each handling a different task or PR, with the main repo untouched.
- The docs page is at `https://code.claude.com/docs` under "Isolate sessions with worktrees."

---

## Hooks

**Current status:** Hooks are shell commands, HTTP endpoints, or LLM prompts that execute at specific lifecycle events in Claude Code; documented in the "Hooks reference" under the Reference section.

**Changes since talk:** The hooks system has been significantly expanded and formalized since the talk. The current docs show:
- Three handler types: shell commands, HTTP endpoints, and LLM prompts (the talk only described shell-command-style hooks).
- Seven distinct events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Stop`, `StopFailure`, `PreToolUse`, `PostToolUse`.
- **Async hooks** are now supported (noted in the reference as an advanced feature).
- **MCP tool hooks** are supported as a distinct hook type.
- Decision control: hooks can return structured JSON to block, modify, or approve tool calls, not just inject content.

**Key details for chapter:**
- Hooks run outside the context window; they inject content only when triggered. This is the zero-overhead abstraction property the speaker described, and it is accurate per the current docs.
- `PreToolUse` and `PostToolUse` fire on every tool call, enabling validation, logging, and gating patterns.
- The hook input arrives via stdin (for command hooks) or POST body (for HTTP hooks) as JSON containing full event context; output can be a decision object to block or modify the tool call.

---

## Skills

**Current status:** Skills are `SKILL.md` files that load into Claude's context only when invoked, either by Claude automatically when relevant or explicitly via `/skill-name` slash command.

**Changes since talk:** Skills appear to be a newer or recently renamed primitive. The docs note: "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way." This consolidation of commands into skills is a post-talk change. The talk described skills as a distinct primitive from slash commands; they are now unified.

**Key details for chapter:**
- Skills are stored in `.claude/skills/<name>/SKILL.md`; the body loads only when the skill is invoked, which is the lazy-loading property that makes them low-overhead for large skill libraries.
- The unification with custom commands means existing `.claude/commands/` files continue to work; no migration required.
- The distinction from `CLAUDE.md`: `CLAUDE.md` is always in context (expensive), skills load on demand (cheap until needed). This is the core context-engineering tradeoff the speaker described.

---

## Sub-agents

**Current status:** Sub-agents are specialized Claude instances with custom system prompts, specific tool access, and independent permissions; each runs in its own context window.

**Changes since talk:** Sub-agents now have a dedicated page ("Create custom subagents") and appear as a first-class feature. The docs reference a "context window visualization" that demonstrates context savings from sub-agent isolation, and an "Agent view" page, both of which suggest tooling for observing agent behavior has been added. "Run agent teams" is a separate page, confirming multi-agent coordination is officially supported.

**Key details for chapter:**
- Sub-agents are defined once and reused; Claude delegates matching tasks automatically based on the subagent's description.
- Each sub-agent has an independent context window; it returns only a summary to the parent, preserving the parent's context budget.
- The recommended pattern for avoiding context flood (the speaker's motivation: "a side task would flood your main conversation with search results") is explicit in the current docs.

---

## Tool Search

**Current status:** The page at `https://docs.anthropic.com/en/docs/claude-code/tool-search` could not be fetched. From the Claude API docs sidebar, "Tool search" appears under "Tool infrastructure" as a distinct page. From training data: tool search allows Claude to search for relevant tools from a large registry rather than having all tool definitions loaded into the system prompt at once, directly addressing the MCP scalability problem the speaker described.

**Changes since talk:** Cannot confirm current state from the fetched docs. The page exists in the API docs sidebar under "Tool infrastructure," which suggests it is a supported API feature. The speaker described tool search as a solution to MCP system-prompt bloat; if this is the same mechanism, it has been formalized as an API-level feature rather than a Claude Code-specific workaround.

**Key details for chapter:**
- Tool search is a mitigation for the system-prompt-bloat problem with large MCP server collections.
- Confirm current URL and feature details at `https://docs.anthropic.com/en/docs/build-with-claude/tool-infrastructure/tool-search` before publication; the fetched page returned an error.
- The speaker's claim that MCP does not scale without tool search (or equivalent lazy-loading) is consistent with what tool search is designed to solve.

---

## Improvement opportunities

- **Diagram: Plugin primitive comparison table.** A side-by-side table comparing MCP, skills, hooks, and sub-agents across four axes: where content lives (system prompt vs. on-demand vs. external), context window impact, scalability in large monorepos, and primary use case. This directly maps to the talk's "four primitives" framing and the zero-overhead abstraction discussion.

- **Diagram: Hook lifecycle flow chart.** A flow chart showing the Claude Code session lifecycle with hook event firing points annotated: `SessionStart` at session open, `UserPromptSubmit` before Claude processes input, `PreToolUse`/`PostToolUse` around each tool call in the agentic loop, and `Stop`/`StopFailure`/`SessionEnd` at termination. Should show which hooks can return decision objects to block or modify execution.

- **Code example: Hooks configuration for zero-overhead context injection.** A `.claude/hooks.json` (or equivalent config) showing a `PreToolUse` hook that runs a shell script only when the tool name matches a pattern, injects relevant context, and returns a structured decision object. Should illustrate the "don't pay for what you don't use" principle with a concrete file-writing or linting enforcement example.

- **Code example: Skills file structure contrasted with CLAUDE.md.** Two files side by side: a bloated `CLAUDE.md` with a long deploy procedure inline, and the equivalent refactored into `.claude/skills/deploy/SKILL.md`. Should show the directory structure and the SKILL.md format, making the lazy-loading benefit concrete.

- **Code example: Automatic prompt caching in a multi-turn agentic session.** A Python snippet using the top-level `cache_control: {"type": "ephemeral"}` parameter with a growing conversation history, plus the `response.usage` output showing `cache_read_input_tokens` vs. `cache_creation_input_tokens`. This makes the "cheap vs. expensive tokens" quote tangible.

- **Worked example: Parallel PR review with git worktrees and sub-agents.** An end-to-end scenario: three open PRs, three worktrees created with `git worktree add`, one Claude Code session per worktree, each session delegating test execution to a sub-agent. Show the shell commands to set up the worktrees and the sub-agent definition file. Maps directly to the slash loop / continuous monitoring workflow the speaker described.

- **Comparison table: KV cache TTL economics.** A table showing base input token price, 5-minute cache write cost (1.25x), 1-hour cache write cost (2x), and cache hit cost (0.1x) for the current main model tiers (Opus 4.x, Sonnet 4.x, Haiku 4.5). Include a break-even column: how many cache hits are needed to recoup a 5-minute write vs. a 1-hour write. This operationalizes the speaker's "cheap vs. expensive tokens" insight.

- **Diagram: Context window composition under different plugin strategies.** A stacked bar visualization showing how the context window fills under three configurations: (1) all MCP tools loaded upfront, (2) skills with lazy loading, (3) hooks injecting only when triggered. Quantify approximate token costs for each layer (system prompt, tool definitions, conversation history, injected context). Makes the Arduino memory analogy from the talk concrete.
