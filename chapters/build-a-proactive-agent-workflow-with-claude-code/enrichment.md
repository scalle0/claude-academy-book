# Enrichment notes: Build a proactive agent workflow with Claude Code

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 2
Pages fetched: 2/2

---

## Claude Code

**Current status:** Claude Code is a generally available AI coding assistant with CLI, VS Code, JetBrains, web, and desktop interfaces, supporting terminal, editor, and remote/web-based workflows.

**Changes since talk:** The talk describes "Routines" as a "brand new feature" being introduced. The fetched overview page does not mention Routines at all. The sidebar navigation shows sections including "Remote Control," "Claude Code on the web," and "Claude Code on desktop," which suggests the product has expanded its surface area considerably. The Routines feature may have shipped under a different name, been folded into another capability, or may still be in limited preview. Cannot confirm current Routines status from the fetched content. The overview page references a `code.claude.com/docs/llms.txt` index, which indicates the documentation has been reorganized since the talk. Third-party provider support for the CLI and VS Code is now documented, which was not mentioned in the talk.

**Key details for chapter:**

- Claude Code now ships across five surfaces: Terminal CLI (installed via `curl -fsSL https://claude.ai/install.sh | bash` or Homebrew/WinGet), VS Code, JetBrains IDEs, a desktop app, and a web interface at code.claude.com. The talk focused on CLI and web; the chapter should acknowledge the full surface area.
- The docs reference a "Remote Control" section and dedicated pages for "Claude Code on the web" and "Claude Code on desktop," which are the surfaces most relevant to hosted/remote session management that Routines relies on.
- Most surfaces require a Claude subscription or Anthropic Console account; third-party provider support is limited to Terminal CLI and VS Code. Routines, as a managed-infrastructure feature, would be subscription-gated.

---

## MCP

**Current status:** The MCP documentation page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404 Not Found response.

**Changes since talk:** The page has moved or been restructured. Based on training data: MCP (Model Context Protocol) is an open protocol Anthropic published that standardizes how applications provide context and tools to LLMs. The talk references "connectors" in Routines as a way to give Claude access to external services; MCP is the underlying mechanism for this. The canonical MCP documentation has likely migrated to a dedicated site (modelcontextprotocol.io) or been reorganized within the Anthropic docs. The chapter should not rely on the URL provided as a stable reference.

**Key details for chapter:**

- MCP defines a client-server protocol where "servers" expose tools, resources, and prompts to LLM clients. In the Routines context, "connectors" are MCP servers that Claude Code can call during an automated session.
- The protocol supports local (stdio) and remote (HTTP/SSE) transport, which is directly relevant to the talk's infrastructure argument: remote MCP servers running on Claude Code's managed infrastructure eliminate the need for users to run local connectors.
- The specification and SDKs are maintained at `modelcontextprotocol.io` (based on training data; verify before publishing). The Anthropic docs page has moved and the old URL should not be cited.

---

## Improvement opportunities

- **Routine definition schema (code example):** A YAML or JSON snippet showing a complete Routine definition with all four components the speaker names: `prompt`, `repos`, `connectors`, and `trigger`. Should include both a cron-style time trigger and a GitHub event trigger variant side by side, since the talk demonstrates both.

- **Trigger type comparison table:** A two-column table contrasting time-based triggers (cron schedule, use cases, latency characteristics) versus event-based triggers (GitHub events, custom webhooks, available event types). The talk distinguishes these clearly but does not enumerate the full set; a table would make this reference-quality.

- **Proactive vs. reactive agent architecture diagram:** A flow diagram contrasting the reactive model (user types prompt, agent responds, session ends) with the proactive Routines model (trigger fires, remote session starts on managed infrastructure, session is observable/steerable via web/CLI/desktop). Emphasizes the "teammate not tool" framing from the talk.

- **Generator-critiquer multi-routine pattern (worked example):** An end-to-end scenario showing two coordinated Routines: Routine A runs weekly, creates a documentation PR; Routine B triggers on `pull_request.opened` events from Routine A's output, reviews and comments before any human sees it. Show the trigger chain explicitly, since the talk describes this pattern but only in one quoted sentence.

- **Context ceiling diagram (figure):** A visual showing the relationship between context inputs (repo access, connectors, prompt specificity) and agent output quality, illustrating the speaker's claim that "whatever context Claude has, that's the ceiling of how successful Claude will be." A pyramid or layered diagram with connector types and repo scope at the base, prompt at the apex, would make this actionable for engineers designing Routines.

- **Infrastructure responsibility comparison table:** Side-by-side table comparing self-hosted agent infrastructure (what the user must manage: compute, session persistence, secret storage, connector auth, retry logic) versus Routines-managed infrastructure (what Claude Code handles vs. what the user still configures). Directly addresses the three challenges named in the talk: deployment complexity, trigger management, and human-in-the-loop interactions.

- **Session interactivity interface comparison (table):** The talk states sessions can be monitored and steered from "web, CLI, and desktop." A table listing each interface, what actions are available (observe, steer mid-run, resume, cancel), and any limitations per surface would be concretely useful given the current docs show these as distinct product pages.

- **MCP connector authentication flow (code example or diagram):** Since the docs URL for MCP is broken, a sequence diagram showing how Routines handles connector authentication on behalf of the user (the managed infrastructure claim) would both explain the architecture and compensate for the missing external reference. Should show token storage, scope, and how the Claude Code session inherits credentials at trigger time.
