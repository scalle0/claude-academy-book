# Enrichment notes: Build AI agents using Claude in Microsoft Foundry

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 2/2

---

## Claude

**Current status:** The current flagship generally available model is Claude Opus 4.7, with Claude Sonnet 4.6 and Claude Haiku 4.5 as the mid-tier and fast options; all three are available on Microsoft Foundry.

**Changes since talk:** The talk references Claude Sonnet 4.6 as the speaker's "current daily driver," which remains a current production model. However, Claude Opus 4.7 has since been released as the top-tier model with a described "step-change improvement in agentic coding" over Opus 4.6. Claude Haiku 4.5 is now the fast-tier model. All current models use a dateless ID format (e.g., `claude-sonnet-4-6`) that is a pinned snapshot, not an evergreen pointer. Context windows are 1M tokens for Opus 4.7 and Sonnet 4.6, 200k for Haiku 4.5. Pricing is $3/$15 per MTok input/output for Sonnet 4.6, $5/$25 for Opus 4.7.

**Key details for chapter:**
- Claude Sonnet 4.6 (`claude-sonnet-4-6`) remains a current production model. Readers building new agentic systems should evaluate Claude Opus 4.7 (`claude-opus-4-7`), which Anthropic specifically positions for complex reasoning and agentic coding.
- All current Claude 4 models are available through Microsoft Foundry using the same model IDs as the Claude API (e.g., `claude-opus-4-7`), not Bedrock-style IDs; model lifecycle follows Anthropic's deprecation schedule, not Microsoft's.
- Claude Sonnet 4.6 supports extended thinking and adaptive thinking; Claude Opus 4.7 supports adaptive thinking but not extended thinking per the current comparison table.

---

## MCP / Model Context Protocol

**Current status:** The page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned 404; the MCP documentation has moved or been reorganized.

**Changes since talk:** The URL provided returned Not Found. From training data and the broader Anthropic docs structure, MCP documentation exists but may have been reorganized under a different path (e.g., `/en/docs/mcp` or within a dedicated MCP section). The canonical MCP specification and SDKs are maintained at `modelcontextprotocol.io` and the `modelcontextprotocol` GitHub org, which are the authoritative sources for the open standard. Anthropic's own MCP docs have historically covered server/client setup, tool definition schemas, and transport types (stdio, HTTP with SSE). The talk's description of MCP as "an open standard for letting AI agents talk to external systems" remains accurate.

**Key details for chapter:**
- The MCP documentation URL used as the entity reference is broken as of fetch time. Link should be verified before publication; check `https://docs.anthropic.com/en/docs/mcp` or the MCP specification at `modelcontextprotocol.io` as alternatives.
- MCP defines a client-server architecture where the AI application acts as the MCP client and external systems expose tools via MCP servers. The tool definition format uses a JSON schema for parameters, which is what Microsoft Agent Framework wraps when referencing the 1,400+ Foundry connectors as MCP tools.
- From training data (caveat: not confirmed against current live docs): MCP supports two primary transport types, stdio (for local process communication, as used in the VS Code local dev workflow shown in the talk) and HTTP with Server-Sent Events (for remote/production deployments).

---

## Improvement opportunities

- **Diagram: Agent architecture overview.** A layered diagram showing the relationship between Claude (model layer), Microsoft Agent Framework (orchestration layer), MCP servers (tool/connector layer), and enterprise systems (SAP, ServiceNow, etc.). Should map directly to the Sparkles cupcake shop demo: user request flows through Foundry to Claude Sonnet 4.6, which plans a multi-step action, calls MCP tools for customer registration and order processing, and returns a response.

- **Comparison table: Claude model selection for agent use cases.** Side-by-side table of Claude Opus 4.7, Sonnet 4.6, and Haiku 4.5 covering: API ID, context window, max output, extended/adaptive thinking support, relative latency, and price per MTok. Include a "recommended for" row mapping to agent task types (complex multi-step reasoning, standard agentic workflows, high-throughput low-latency tasks).

- **Code example: MCP server tool definition.** A minimal MCP server stub showing a tool definition in JSON schema format for one of the Sparkles demo tools (e.g., `register_customer` with fields for name, email, and order preferences). Should show the `name`, `description`, and `inputSchema` fields that Claude uses during tool selection in the agent loop.

- **Code example: Microsoft Agent Framework agent initialization.** A Python or C# snippet showing the minimum code to instantiate an agent against Claude Sonnet 4.6 via Foundry, attach an MCP server, and send the first user message. The talk claims "minimal code requirements"; a working skeleton would substantiate that claim and give readers a copy-paste starting point.

- **Diagram: Prototype-to-production path in Foundry.** A flow chart showing the three stages described in the talk: Foundry playground (zero-code model testing), local VS Code development (agent logic with MCP), and production deployment (Foundry-managed scaling with Defender/Purview/EntraID). Annotate each stage with what is added (observability hooks, security policies, governance controls).

- **Worked example: Multi-step reasoning trace.** Walk through the Sparkles order scenario as a concrete agent execution trace: input message, Claude's internal plan, tool calls issued (with request/response payloads), follow-up reasoning, and final response. This makes the "planning, reasoning, and taking action" claim concrete and shows how Claude handles ambiguous or incomplete customer input mid-conversation.

- **Comparison table: Build-vs-buy for agent infrastructure.** A table comparing building a custom agent platform (bring-your-own orchestration, auth, observability, connectors) against using Microsoft Foundry. Rows: connector count, security integration, observability tooling, deployment complexity, time-to-production. This gives the chapter a factual basis for the quote about not building "your own platform from scratch."
