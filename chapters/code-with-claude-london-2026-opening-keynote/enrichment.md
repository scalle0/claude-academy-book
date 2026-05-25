# Enrichment notes: Code with Claude London 2026: Opening Keynote

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 4
Pages fetched: 4/4

---

## Claude Code

**Current status:** Claude Code is a generally available AI-powered coding assistant with a CLI, desktop app, VS Code/JetBrains integrations, web interface, and an Agent SDK, installable via `curl -fsSL https://claude.ai/install.sh | bash`.

**Changes since talk:** The documentation shows several surfaces the talk may have been previewing or announcing: a desktop app (for multi-session management, which the talk describes as a new feature), a web interface ("Claude Code on the web"), a Chrome extension in beta, and a "Computer use (preview)" integration within Claude Code specifically. The Agent SDK is listed as a distinct section. The install method is now a unified shell script rather than npm. "Routines" as a named feature for asynchronous development is not reflected in current docs under that term, suggesting it may have been renamed, not yet shipped, or described under a different heading (e.g., session management or the Agent SDK).

**Key details for chapter:**
- Claude Code supports multiple installation surfaces: terminal CLI, VS Code, JetBrains, desktop app, and web, each requiring a Claude subscription or Anthropic Console account.
- The desktop app is now documented as a shipping feature, consistent with the talk's framing of it as a multi-session management tool.
- The Agent SDK is a distinct documented layer, relevant to the talk's discussion of managed agents and multi-agent orchestration.

---

## MCP

**Current status:** The MCP page at the provided URL returned a 404/Not Found, meaning the documentation has moved or the path is no longer valid.

**Changes since talk:** The MCP content has been reorganized. Based on what rendered in the navigation sidebar of adjacent pages (computer use, tool use), MCP now lives under a section containing "Remote MCP servers," "MCP connector," and "MCP tunnels." The old path `agents-and-tools/model-context-protocol` is gone. The canonical entry point for building MCP clients is now listed as `modelcontextprotocol.io`, an external site. The tool-use overview explicitly states: "For connecting to MCP servers, see the MCP connector." This is a meaningful structural change: MCP client concerns have been externalized to the protocol's own site, while Anthropic's docs focus on the connector/server side.

**Key details for chapter:**
- The MCP docs path has changed; readers should use the "MCP" section in the current API docs sidebar, which covers remote MCP servers, the MCP connector, and MCP tunnels.
- The MCP connector is now the documented integration point for connecting Claude to MCP servers from API calls; the tool-use overview cross-references it directly.
- For building custom MCP clients, the current docs redirect to `modelcontextprotocol.io` rather than Anthropic-maintained documentation.

---

## computer use

**Current status:** Computer use is a beta feature providing screenshot capture, mouse/keyboard control, and desktop automation via the `computer_20251124` tool type, requiring beta header `computer-use-2025-11-24` for current models.

**Changes since talk:** Two beta header versions now exist: `computer-use-2025-11-24` for Claude Opus 4.7, Opus 4.6, Sonnet 4.6, and Opus 4.5; and the older `computer-use-2025-01-24` for Claude Sonnet 4.5, Haiku 4.5, Opus 4.1, and deprecated Sonnet 4/Opus 4. The tool type string is `computer_20251124`. Claude Opus 4.7 is the current recommended model (used in the quick-start example). A prompt injection classifier layer has been added: when classifiers detect potential prompt injections in screenshots, they automatically prompt for user confirmation before proceeding. This classifier defense is opt-out via support request. The feature is now eligible for Zero Data Retention. Computer use is also listed as a distinct integration within Claude Code ("Computer use (preview)"), separate from the API-level feature.

**Key details for chapter:**
- Use beta header `computer-use-2025-11-24` with `claude-opus-4-7` for current deployments; the older `computer-use-2025-01-24` header covers earlier models including now-deprecated Sonnet 4 and Opus 4.
- Anthropic now runs automatic prompt injection classifiers on screenshots during computer use sessions; this is enabled by default and can be disabled by contacting support.
- Computer use is now accessible both via the Messages API and as a preview integration inside Claude Code, creating two distinct deployment paths.

---

## tool use

**Current status:** Tool use lets Claude call client-defined functions or Anthropic-hosted server tools, with the primary architectural distinction being where execution happens: client tools return `stop_reason: "tool_use"` for your code to handle, while server tools (web search, code execution, web fetch, tool search) execute on Anthropic infrastructure.

**Changes since talk:** The tool catalog has expanded significantly. Server tools now include: `web_search_20260209` (note the 2026 date in the type string), `code_execution`, `web_fetch`, and `tool_search`. An "Advisor tool" is listed as a named server tool, which directly corresponds to the talk's "advisor strategy" claim about using a larger advisor model with a smaller execution model. A "Memory tool" and "Tool Runner (SDK)" are also new additions. Strict tool use (`strict: true`) is now a documented feature guaranteeing schema conformance. The tool-use system prompt token overhead is documented per-model: Claude Opus 4.7 costs 346 tokens for `auto`/`none` and 313 tokens for `any`/specific tool. The current model in examples is `claude-opus-4-7`.

**Key details for chapter:**
- The advisor strategy described in the talk maps to a literal "Advisor tool" now listed in the server tools section; this is not just an architectural pattern but a shipped API primitive.
- Tool type strings carry dates (e.g., `web_search_20260209`) that version the tool interface; code must use the correct versioned string.
- Strict tool use (`strict: true` on tool definitions) is available to guarantee Claude's output matches the provided JSON schema exactly, relevant to the talk's discussion of reducing scaffolding complexity.

---

## Improvement opportunities

- **Advisor strategy, comparison table:** A side-by-side table showing the advisor pattern versus standard single-model calls, with columns for model pairing (e.g., Haiku executor + Opus advisor), relative cost multiplier, latency tradeoff, and recommended use case. The talk claims 5x cost reduction; the table should ground that claim in current model pricing from the models overview.

- **Tool use, code example:** A minimal Python example showing the advisor tool invoked alongside a smaller execution model, using the `client.messages.create` pattern from the current docs, to make the "frontier quality at 5x lower cost" claim concrete and reproducible.

- **MCP, diagram:** An architecture diagram showing the three integration paths the talk implies: (1) Claude Code connecting to an MCP server directly, (2) API calls using the MCP connector, and (3) remote MCP servers via MCP tunnels. Include the URL reorganization note so readers know the old `agents-and-tools/model-context-protocol` path is dead.

- **Computer use, code example:** The reference implementation quick-start from the current docs, trimmed and annotated, showing the `computer_20251124` tool definition with correct beta header, alongside a note on which models require which header version. The talk uses computer use as a capability demonstration anchor; readers need the exact invocation.

- **Task horizon, comparison table:** A table mapping the talk's "task horizon" metric across time: last year (minutes), current (hours), and projected (continuous/proactive). Cross-reference with concrete agent loop configurations, maximum token budgets, and session management features in Claude Code, to turn a rhetorical metric into an operational one.

- **Claude Code surfaces, diagram:** A deployment topology diagram showing all current Claude Code surfaces (terminal CLI, desktop app, VS Code, JetBrains, web, Chrome extension) with the install method for each and which require a Console account versus a Claude subscription. The talk distinguishes Claude Code as a product layer; readers need to know which surface to target for which use case.

- **Strict tool use, worked example:** An end-to-end scenario showing a migration pipeline (referencing the Spotify 1,000-PR/month example from the talk) where `strict: true` on tool definitions prevents schema drift across a multi-step agentic workflow, with the tool definition JSON and a sample tool call/result exchange.

- **Scaffolding reduction, before/after code example:** Two versions of a multi-step agent loop: one with heavy custom scaffolding (explicit state machines, retry logic, intermediate validation) and one using generalized primitives (server tools, the Tool Runner SDK, and compaction), illustrating the talk's claim that "more intelligent models can get further with generalised primitives."
