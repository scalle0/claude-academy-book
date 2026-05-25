# Enrichment notes: How to get to production faster with Claude Managed Agents

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 4
Pages fetched: 4/4

---

## Claude Code

**Current status:** Claude Code is a standalone agentic coding assistant available as a CLI, VS Code extension, desktop app, web interface, and JetBrains plugin, documented at code.claude.com.

**Changes since talk:** The talk discusses Claude Code as an example of agent capabilities (clearing backlogs, generating merge-ready PRs). The current docs show substantial surface expansion since any early-stage recording: Claude Code now has a dedicated Agent SDK, a skills system (see below), hooks for automation, scheduled prompt execution, external event push, subagent creation, worktree isolation, and a "Remote Control" integration. The product has moved well past "coding assistant" into a full agent platform with its own orchestration primitives.

**Key details for chapter:**
- Claude Code exposes an Agent SDK for programmatic session control, not just interactive use.
- The platform supports parallel agent teams via subagents with isolated worktrees, which directly maps to the multi-agent orchestration concept the talk describes.
- Deployment surfaces now include CI/CD integration and Slack, meaning agents can be triggered from external systems without a human at the terminal.

---

## MCP

**Current status:** The MCP page at `docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404/Not Found response.

**Changes since talk:** The page failed to fetch. Based on training data: MCP (Model Context Protocol) is an open protocol Anthropic introduced for standardizing how tools and context sources connect to models. The talk references MCP Tunnels as a new feature enabling secure access to private MCP servers without public internet exposure. The current canonical MCP documentation appears to have moved or been restructured; the Claude Code docs sidebar shows MCP under "Tools and plugins > Model Context Protocol (MCP)" at `code.claude.com`, suggesting the primary MCP reference for Claude Code users has migrated to that domain. Treat any claims about the MCP docs URL in the chapter as potentially stale.

**Key details for chapter:**
- The MCP documentation URL used in the talk's context (`docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol`) no longer resolves; the active reference is under the Claude Code docs at `code.claude.com`.
- MCP Tunnels, described in the talk as a new announcement for private server access within VPCs, should be verified against current docs before the chapter goes to print, as the feature may have GA'd or changed scope.
- The "Discover and install prebuilt plugins" and "Create plugins" entries in the Claude Code sidebar suggest MCP server management is now framed through a plugin model rather than raw protocol configuration.

---

## memory

**Current status:** Claude Code memory is documented at `code.claude.com/docs/claude-code/memory` and covers two mechanisms: CLAUDE.md files (human-authored persistent instructions) and auto memory (Claude-authored notes from corrections and preferences).

**Changes since talk:** The talk describes memory as a platform-level primitive for agents needing cross-session persistence, analogous to human memory. The current docs scope memory specifically to Claude Code sessions via file-based mechanisms. Auto memory (Claude writing its own notes) is a current feature. The `.claude/rules/` directory for file-type-scoped rules is a current addition not likely present at early recording dates. No deprecated functionality detected.

**Key details for chapter:**
- Memory operates through two distinct channels: CLAUDE.md files for developer-controlled instructions, and auto memory for Claude-generated notes, both loaded at session start into the context window.
- Rules can be scoped to specific file types using `.claude/rules/`, giving per-filetype instruction granularity.
- Memory content is loaded as context, not enforced configuration; specificity and conciseness directly determine how reliably instructions are followed.

---

## skills

**Current status:** Skills are Claude Code's mechanism for packaging reusable multi-step procedures as SKILL.md files, invocable via `/skill-name`, stored under `.claude/skills/`.

**Changes since talk:** The talk uses "skills" as one of the composable primitives in agent definitions (alongside system prompts, models, tools, permissions). The current docs show that custom commands have been merged into skills: a file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` are now equivalent. This is a consolidation that post-dates earlier documentation and may differ from what the talk described. Skills load their body only when invoked, keeping them out of the baseline context window cost.

**Key details for chapter:**
- A skill's body is not loaded into the context window until the skill is invoked, making long reference procedures cost-free at session start.
- Custom commands (`.claude/commands/*.md`) and skills (`.claude/skills/*/SKILL.md`) are now unified; the chapter should not describe them as separate concepts.
- Skills are the recommended refactoring target when a CLAUDE.md section grows into a procedure rather than a fact, providing a clear authoring heuristic.

---

## Improvement opportunities

- **Agent definition schema, code example:** Show a complete agent definition object with all five components the talk names (system prompt, model, skills, tools, permissions) as a JSON or YAML block. The talk lists these primitives verbally but a concrete structure would ground the concept for engineers building their first agent.

- **Multi-agent orchestration, architecture diagram:** A diagram showing a root agent spawning two or three specialized subagent threads with separate context windows, with arrows indicating task delegation and result return. The talk describes this pattern in one sentence; a visual would clarify how context isolation actually works across threads.

- **CLAUDE.md vs auto memory vs skills, comparison table:** A three-column table with rows for authorship (human vs Claude), load timing (always vs on-invoke), persistence mechanism (file path), and primary use case. The talk conflates memory and skills as agent primitives; the table would clarify where each fits in the stack.

- **MCP Tunnels, worked example:** An end-to-end scenario showing a private MCP server inside a corporate VPC, the tunnel configuration, and how the agent accesses tools from it without a public endpoint. The talk announces this as a new feature but gives no implementation detail; this is the highest-value gap for engineers evaluating private deployment.

- **Self-hosted sandbox, architecture diagram:** A diagram contrasting Anthropic-hosted sandbox execution against a customer VPC deployment, labeling the security boundary, what compute runs where, and what calls cross the boundary. The talk names this as a new announcement without showing the topology.

- **Interaction paradigm comparison table:** A table with three rows (conversational, outcome-oriented, asynchronous) and columns for trigger mechanism, response model, typical use case, and session lifetime. The talk names all three paradigms but treats them as a verbal list; a table makes the tradeoffs scannable.

- **Event streaming, code example:** A code snippet showing how to consume the session event stream, with example event types (user turn, Claude response, tool call, tool result) and a minimal handler. The talk describes events as the core observability primitive but gives no API surface detail.

- **Skills invocation, code example:** A minimal SKILL.md file alongside the corresponding `/skill-name` invocation, showing the file path convention, frontmatter if any, and how Claude loads it on demand versus CLAUDE.md at session start. This directly illustrates the lazy-loading cost model the docs describe.
