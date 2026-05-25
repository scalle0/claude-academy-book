# Enrichment notes: Build a production-ready agent with Claude Managed Agents

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 3/3

---

## Claude Code

**Current status:** Claude Code is an AI-powered coding assistant available as a CLI, VS Code extension, desktop app, web interface, and JetBrains plugin that operates on your codebase across files and tools.

**Changes since talk:** The talk does not discuss Claude Code directly; it appears in the enrichment entities list but is not referenced in the chapter summary or quotes. The fetched documentation confirms Claude Code is a distinct product (coding assistant) unrelated to the managed agents infrastructure described in this talk. Flag this entity as likely misassigned to this chapter.

**Key details for chapter:**
- Claude Code is a separate product from Claude Managed Agents; the two are not the same offering and should not be conflated in chapter text.
- If the chapter references Claude Code as an example of an agent built on managed infrastructure, note that the public documentation does not describe it that way; no such claim is supported by current docs.
- The Claude Code docs live at `code.claude.com/docs` and `docs.anthropic.com/en/docs/claude-code/overview`, not under the agents-and-tools namespace where managed agent primitives are documented.

---

## MCP

**Current status:** The MCP documentation page at `docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404/Not Found, so no current content could be fetched from that URL.

**Changes since talk:** The page at the provided URL no longer exists. Based on the tool-use overview page fetched successfully, MCP is now documented under a dedicated "MCP" section in the sidebar with subsections: Remote MCP servers, MCP connector, and MCP tunnels. The old URL `agents-and-tools/model-context-protocol` has been reorganized. The talk mentions "MCP tunnels" as a mechanism for connecting private data sources, and MCP tunnels now appear as a named, documented subsection, suggesting the concept has been formalized and promoted to a first-class feature.

**Key details for chapter:**
- MCP documentation has moved; the current canonical entry points are the MCP connector doc and the MCP tunnels doc, accessible from the tool-use sidebar under the "MCP" grouping.
- The talk's description of MCP tunnels as a way to expose private data sources without putting them on the internet aligns with the current "MCP tunnels" subsection title, so the core concept holds but should be linked to the new URL.
- `modelcontextprotocol.io` is cited in current docs as the reference for building your own MCP client, distinct from using Anthropic's MCP connector endpoint.

---

## tool use

**Current status:** Tool use allows Claude to call developer-defined functions (client tools) or Anthropic-hosted functions (server tools), with Claude deciding invocation based on request context and tool descriptions.

**Changes since talk:** Several additions are notable. The docs now distinguish explicitly between client tools and server tools as a first-class conceptual split; the talk predates this framing being this prominent. Anthropic now provides named server tools: `web_search`, `code_execution`, `web_fetch`, and an advisor tool, memory tool, bash tool, computer use tool, and text editor tool. A `strict: true` parameter is available on tool definitions to enforce schema conformance. The Tool Runner (SDK) is a documented feature. Per-tool permission controls described in the talk (auto-execute vs. require approval) align conceptually with current docs but are not described in exactly that framing in the current overview. Current model names in the pricing table include Claude Opus 4.7, Claude Sonnet 4.6, Claude Haiku 4.5 as active models; Claude Haiku 3.5 is retired except on Bedrock and Vertex AI.

**Key details for chapter:**
- The client/server tool distinction is now the primary organizational frame: client tools run in your application and return `stop_reason: "tool_use"` requiring your code to execute; server tools run on Anthropic infrastructure and return results directly without a round-trip.
- Token overhead for tool use is non-trivial: the tool-use system prompt adds 346 tokens (auto/none) or 313 tokens (any/tool) per request for current Opus and Sonnet 4.x models, in addition to schema tokens and `tool_use`/`tool_result` blocks.
- `strict: true` on tool definitions enforces schema conformance, directly relevant to the production-reliability claims in the talk.

---

## Improvement opportunities

- **Diagram: agent primitive relationships.** An architectural diagram showing how agents, environments, sessions, and events relate to each other as a hierarchy or flow. Should show: a session containing multiple agent turns, events emitted at each stage (user events, agent events, span events, session events), and where MCP tunnels and credential vaults attach to the environment layer.

- **Code example: session creation with per-tool permission controls.** An API call showing how to define a toolset where `file_read` is set to auto-execute and a database MCP tool requires explicit approval. Directly illustrates the quote about granular permission controls and would be the most-cited snippet in this chapter.

- **Code example: MCP tunnel configuration for a private data source.** A minimal config showing how to register a self-hosted MCP server via tunnel, including where credentials are referenced from the vault rather than passed inline. Addresses the "without Claude ever seeing what those things are" claim with a concrete artifact.

- **Comparison table: client tools vs. server tools.** Side-by-side table with columns: execution location, who handles the loop, latency characteristics, authentication model, example tools. The talk's demo uses both types implicitly; making the distinction explicit helps readers choose the right approach for their deal desk or similar application.

- **Worked example: multi-agent deal desk flow.** End-to-end walkthrough of the demo from the talk: one orchestrating agent spawning a financial analysis sub-agent and a company research sub-agent, each with different personas and tool access, converging results into a session. Should show the API calls for spawning sub-agents and how outcome events drive iteration.

- **Diagram: event taxonomy.** A categorized list or tree diagram of the four event types (user events, agent events, session events, span events) with one concrete example of each and when each fires in the agent lifecycle. The talk names these but does not enumerate examples in the summary.

- **Code example: memory store read/write pattern.** A snippet showing an agent writing a memory at session end and reading it at session start, illustrating how the persistent knowledge claim works at the API level rather than as a conceptual description.

- **Comparison table: self-hosted environment vs. Anthropic-hosted sandbox.** Two-column table covering: infrastructure ownership, data residency, latency to private resources, setup complexity, and relevant use cases. The talk's quote about bringing your own sandboxes is a selling point for enterprise readers who cannot route data through Anthropic infrastructure.
