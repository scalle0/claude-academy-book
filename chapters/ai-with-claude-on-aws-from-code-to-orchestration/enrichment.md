# Enrichment notes: AI with Claude on AWS: From code to orchestration

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 6
Pages fetched: 6/6

---

## Claude Code

**Current status:** Claude Code is a generally available AI-powered coding assistant deployable across terminal, VS Code, desktop app, web, and JetBrains IDEs, with support for third-party model providers including AWS Bedrock.

**Changes since talk:** The docs now live at `code.claude.com/docs` (also accessible via `docs.anthropic.com/en/docs/claude-code`). The product has expanded significantly: it now has a full Agent SDK, a dedicated web surface, a Chrome extension (beta), computer use (preview), and remote control capabilities. The sidebar structure reveals sub-products that may not have existed at talk time, including Claude Code on the web and the Chrome extension.

**Key details for chapter:**
- Third-party provider support (including AWS Bedrock) is explicitly listed as available for the Terminal CLI and VS Code surfaces, which is the integration path described in the workshop.
- The docs index lives at `https://code.claude.com/docs/llms.txt`, useful for programmatic discovery of current feature surface.
- Installation on macOS/Linux/WSL is `curl -fsSL https://claude.ai/install.sh | bash`; Homebrew and WinGet are also supported.

---

## MCP

**Current status:** The `docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` URL returned a 404; the MCP documentation has moved or been restructured.

**Changes since talk:** The page did not load. Based on the Claude Code docs sidebar (which fetched successfully), MCP is now documented under the Claude Code docs at `code.claude.com/docs` under "Tools and plugins > Model Context Protocol (MCP)" rather than as a top-level agents-and-tools page. The talk described MCP as the integration mechanism for tools like the Playwright screenshot workflow; this positioning appears consistent with current docs, but the URL the chapter references is stale.

**Key details for chapter:**
- Use the current MCP docs location under Claude Code's "Tools and plugins" section, not the `agents-and-tools` path.
- MCP is described in the Claude Code sidebar alongside "Discover and install prebuilt plugins" and "Create plugins," indicating the ecosystem has matured with a plugin marketplace layer on top of raw MCP.
- The Playwright MCP use case described in the workshop (automated screenshot workflow) aligns with the prebuilt plugin discovery path now documented.

---

## fine-tuning

**Current status:** The `docs.anthropic.com/en/docs/build-with-claude/fine-tuning` URL returned a 404; this page no longer exists at this path.

**Changes since talk:** The page did not load. The talk's claim that AWS/Bedrock is "the only provider that can provide" Claude fine-tuning (specifically Haiku) cannot be verified against current Anthropic docs. This is a significant flag: the fine-tuning page may have been removed, the feature may have moved to Bedrock-specific documentation entirely, or the URL has changed. The chapter should not present fine-tuning via Bedrock as current without verifying against AWS Bedrock docs directly.

**Key details for chapter:**
- Treat the fine-tuning claim as unverified until the AWS Bedrock documentation is checked. The Anthropic-side fine-tuning docs page is currently missing.
- If the chapter repeats the "only provider for fine-tuning" claim, it needs a sourced caveat, since this competitive claim cannot be confirmed from current Anthropic docs.
- The model the speaker cited for fine-tuning was Claude Haiku; verify current model availability for fine-tuning against Bedrock's current model catalog, as Haiku versions have iterated (claude-haiku-3, claude-haiku-3-5).

---

## hooks

**Current status:** Hooks are a stable, documented Claude Code feature that execute user-defined shell commands, HTTP endpoints, or LLM prompts at specific lifecycle events in a Claude Code session.

**Changes since talk:** The hooks system has grown substantially. Current docs describe seven distinct events: `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Stop`, `StopFailure`, `PreToolUse`, and `PostToolUse`. The docs now cover async hooks, HTTP hooks, and MCP tool hooks as distinct variants. A separate guide ("Automate workflows with hooks") exists alongside the reference page. The level of detail suggests this is more mature than what would have been available at an early workshop demo.

**Key details for chapter:**
- Hooks fire at three cadences: once per session (`SessionStart`, `SessionEnd`), once per turn (`UserPromptSubmit`, `Stop`, `StopFailure`), and on every tool call inside the agentic loop (`PreToolUse`, `PostToolUse`).
- Three handler types are supported: shell commands (stdin delivery), HTTP endpoints (POST body delivery), and LLM prompts.
- Hooks can return a decision (allow/block), not just perform side effects, making them usable for policy enforcement, not just logging or notification.

---

## skills

**Current status:** Skills are Claude Code's mechanism for packaging reusable instruction sets as slash-command-invocable procedures, defined via a `SKILL.md` file in `.claude/skills/<name>/`.

**Changes since talk:** The term "custom commands" has been merged into skills. The docs explicitly state: "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way." If the talk referred to "custom commands" as a separate concept, that distinction no longer exists. Skills also differ from CLAUDE.md content in that their body loads only when invoked, so they do not consume context until used.

**Key details for chapter:**
- Skill definition path: `.claude/skills/<name>/SKILL.md`. Legacy `.claude/commands/<name>.md` still works and creates the same slash command.
- Skills load lazily: content is not injected into the context window until the skill is invoked, which matters for managing context budget in long sessions.
- Built-in skills include `/debug` and `/code-review`; custom skills extend this same invocation interface.

---

## sub-agents

**Current status:** Sub-agents (now spelled "subagents" in current docs) are specialized Claude Code assistants that run in isolated context windows with custom system prompts, specific tool access, and independent permissions, invoked automatically when Claude matches a task to a subagent's description.

**Changes since talk:** The current docs use "subagents" (one word, no hyphen) rather than "sub-agents." The feature is documented as part of a broader "Agents and parallel work" section that also includes "Run agent teams," "Agent view," and "Isolate sessions with worktrees," indicating the multi-agent orchestration surface has expanded beyond basic sub-agent delegation. The context window visualization tool is now referenced as a companion resource for understanding subagent context savings.

**Key details for chapter:**
- Each subagent runs in its own context window; the parent agent receives only the summary, not the raw output. This is the primary use case: preventing log/search result floods in the main context.
- Subagents are defined by a custom system prompt plus specific tool restrictions and permission sets, not just a role description.
- The "Agents and parallel work" section now includes worktree isolation and agent teams, suggesting the talk's workshop covered an early version of a now-larger orchestration model.

---

## Improvement opportunities

- **Comparison table: Three AWS deployment methods.** The talk describes three distinct ways to access Claude on AWS (Amazon Bedrock direct, Claude Platform gateway, AWS Marketplace desktop). A table with columns for deployment method, feature parity with Anthropic direct, fine-tuning availability, network isolation options, and compliance certifications would make the tradeoffs concrete and referenceable.

- **Code example: Claude Code with AWS Bedrock provider config.** The workshop covers configuring Claude Code to use Bedrock as the model provider. Show the minimal configuration (environment variables or `.claude` config file) required to point Claude Code at a Bedrock endpoint, including the `ANTHROPIC_MODEL` or equivalent override and the AWS credential chain it uses. This is the most actionable thing a reader will want to reproduce.

- **Code example: MCP server config for Playwright screenshot workflow.** The workshop demo uses Playwright MCP for automated screenshots. Show the `.claude/mcp.json` or equivalent config block that registers a local Playwright MCP server, including the `command`, `args`, and any `env` fields, so readers can reproduce the specific demo described.

- **Code example: PreToolUse hook for policy enforcement.** The hooks section of the workshop is described as an advanced feature. Show a concrete `hooks` config block that fires on `PreToolUse`, checks the tool name against an allowlist, and returns a block decision with a reason string. This illustrates the enforcement use case rather than just the notification use case.

- **Worked example: Subagent definition for a research task.** The workshop covers sub-agents as a way to isolate long-running tasks. Walk through creating a `.claude/agents/` YAML definition for a documentation-search subagent scoped to read-only tools, showing how the parent session invokes it and receives a summary, using the Scaledraw/AWS context from the demo.

- **Diagram: Claude Code feature dependency map.** Draw a single figure showing how MCP, skills, hooks, and subagents relate to the core agentic loop. MCP provides tools; skills provide slash-command procedures; hooks intercept lifecycle events; subagents run isolated loops. Without this, the relationship between these four extension points is not obvious from the talk narrative.

- **Diagram: AWS Claude deployment architecture.** Show the network path from a customer VPC to a Claude model on Bedrock, including Private Link, the zero-operator-access boundary, the Trainium compute layer, and where fine-tuning artifacts live. This makes the security and infrastructure claims (FedRAMP, HIPAA, zero operator access) spatially concrete.

- **Comparison table: skills vs. CLAUDE.md vs. hooks for recurring workflows.** The talk covers all three as mechanisms for customizing Claude Code behavior, but the docs reveal they serve different purposes (persistent context vs. lazy-loaded procedures vs. event-triggered side effects). A table with rows for each mechanism and columns for when it loads, whether it consumes context, how it is invoked, and best-fit use case would help readers pick the right tool.
