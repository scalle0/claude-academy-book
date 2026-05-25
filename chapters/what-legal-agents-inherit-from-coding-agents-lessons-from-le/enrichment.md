# Enrichment notes: What legal agents inherit from coding agents: Lessons from Legora

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 3/3

---

## Claude Code

**Current status:** Claude Code is a generally available agentic coding assistant deployed as a CLI, VS Code extension, JetBrains plugin, desktop app, and web interface, supporting terminal automation, multi-file editing, and agent/subagent workflows.

**Changes since talk:** The talk references Claude Code as a reference model for agentic patterns (planning, human-in-the-loop, sub-agents, sandboxes). The product has expanded significantly: the web surface, desktop app, Chrome extension (beta), computer use (preview), and Slack integration are all listed in current docs. The Agent SDK and scheduled prompts are also present. None of these additions contradict the talk's claims; they extend the same patterns the speaker described. No deprecated functionality relevant to the talk's arguments.

**Key details for chapter:**

- Claude Code's architecture explicitly supports the read-edit-verify loop the speaker identifies as the core translatable pattern: it operates across files and tools within a single agent context, not a multi-model handoff chain.
- The platform exposes subagents, hooks, MCP plugins, and permission modes as first-class primitives, which maps directly to the speaker's "reuse one to one" bucket (sub-agents, sandboxes, human-in-the-loop).
- Current docs live at `https://docs.anthropic.com/en/docs/claude-code/overview`; the full index is fetchable from `https://code.claude.com/docs/llms.txt`.

---

## citations

**Current status:** The Citations API is a production Messages API feature that attaches source-verified inline citations to Claude responses over plain text, PDF, and custom content documents, with `cited_text` excluded from output token billing.

**Changes since talk:** The citations feature is materially more capable than a basic "include a source pointer" approach. Key current details worth noting for the chapter: (1) citations are incompatible with Structured Outputs -- enabling both returns a 400 error; (2) Haiku 3 does not support citations; (3) `cited_text` does not count toward output tokens and is also not counted as input tokens when passed back in subsequent turns; (4) custom content documents allow caller-controlled chunking granularity, which is directly relevant to legal document workflows where sentence-level chunking may be wrong (e.g., clause-level or defined-term-level is more appropriate). No renamed concepts since the talk.

**Key details for chapter:**

- Enable citations per-document via `citations: { enabled: true }` on each document block; citations must be enabled on all or none of the documents in a request.
- Three document types are supported: plain text (auto sentence-chunked), PDF (auto sentence-chunked, images not citable), and custom content (caller defines chunk boundaries, no further chunking applied). For legal documents with non-standard structure, custom content is the right choice.
- Citations integrate with prompt caching: apply `cache_control` to document blocks to cache source material across turns while still generating fresh citations per response.

---

## sub-agents

**Current status:** Claude Code sub-agents are a first-class feature allowing definition of specialized agents with custom system prompts, scoped tool access, and independent context windows; they are spawned by the orchestrating agent when a task matches the subagent's description.

**Changes since talk:** The speaker listed "sub-agents" in the direct-reuse bucket without elaboration. Current docs make the architecture explicit: each subagent runs in its own context window, which means it does not pollute the orchestrator's context with intermediate artifacts (search results, file contents, logs). This is now documented as the primary motivation for using subagents, not just parallelism. The "Agent view" and "Run agent teams" pages indicate UI-level visibility into subagent execution, which did not exist at the likely talk date.

**Key details for chapter:**

- Subagents are defined with a system prompt, a tool allowlist, and an independent permission set; the orchestrator delegates by description match, not by explicit API call.
- The isolation property -- subagent work stays in its own context window and only a summary returns to the orchestrator -- is directly analogous to Legora's motivation for avoiding multi-model handoff: keeping context clean and reasoning coherent.
- Custom subagents are persistent definitions (not ephemeral spawns), making them appropriate for recurring task types like "run a due diligence checklist on this document" or "extract structured data from this contract."

---

## Improvement opportunities

- **Comparison table -- three-bucket framework vs. Claude Code primitives:** A side-by-side table mapping Legora's three buckets (reuse, translate, invent) to specific Claude Code features. Columns: Bucket | Legora example | Claude Code primitive | Docs reference. Rows cover: planning/TodoWrite, subagents, sandboxes, human-in-the-loop permission modes, the read-edit-verify loop, and citations.

- **Diagram -- single-agent loop vs. multi-model handoff architecture:** A flow diagram contrasting Legora's old architecture (multiple LLMs, independent context, handoff points) against the translated single-agent read-edit-verify loop. Should show where context is shared, where reasoning is independent, and where verification happens. Annotate the handoff failure modes the speaker names.

- **Code example -- citations API call on a legal document with custom chunking:** A Python snippet using the Messages API with a custom content document (not plain text), `citations: { enabled: true }`, and `cache_control` on the document block. Should demonstrate clause-level chunk boundaries rather than auto sentence chunking, since legal documents have clause/section structure that sentence chunking handles poorly.

- **Code example -- subagent definition for a recurring legal task:** A Claude Code subagent config (system prompt + tool list) for a due diligence subagent. Should show how the orchestrator delegates by description and how only the structured summary returns to the main context, not the full document contents.

- **Diagram -- intermediate document representation layer:** A diagram showing how DOCX (ZIP of XML) is converted to an intermediate representation, edited by the agent loop, then rendered back. Should call out where the "linting" step fits (post-edit, pre-render) and map it to the ESLint analogy from the talk.

- **Comparison table -- citation chunking strategies for legal documents:** Table comparing auto sentence chunking vs. custom content chunking for legal document types. Columns: Document type | Default chunking unit | Problem for legal work | Recommended approach. Rows: contracts, case law excerpts, regulatory text, due diligence checklists.

- **Worked example -- approval workflow for dangerous legal actions:** End-to-end scenario showing a human-in-the-loop interrupt when the agent proposes an action above a risk threshold (e.g., accepting a liability clause). Should map to Claude Code's permission modes and show the structured approval request format.
