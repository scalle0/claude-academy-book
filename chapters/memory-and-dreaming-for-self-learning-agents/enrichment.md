# Enrichment notes: Memory and dreaming for self learning agents

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 7
Pages fetched: 5/5

---

## Claude

**Current status:** Claude Opus 4.7 is the current flagship model; the model lineup spans Opus 4.7, Sonnet 4.6, and Haiku 4.5, all with 1M token context windows except Haiku 4.5 (200k).

**Changes since talk:** The talk references Claude's file navigation and grep capabilities in the context of memory architecture, not a specific model version. Model generations have advanced significantly since any plausible talk date. Current flagship is claude-opus-4-7, described as having "a step-change improvement in agentic coding." Context windows for Opus and Sonnet are now 1M tokens. Model ID versioning convention changed at the 4.6 generation: IDs no longer include dates and are pinned snapshots rather than evergreen pointers.

**Key details for chapter:**
- Current production models: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`. Use these IDs when citing model capabilities relevant to memory and file manipulation.
- Context window for Opus and Sonnet is 1M tokens; relevant when discussing how much session transcript a dreaming process can analyze in a single pass.
- Agentic coding is a stated emphasis for Opus 4.7, directly relevant to the chapter's claims about file system navigation as memory substrate.

---

## Claude Code

**Current status:** Claude Code is a generally available AI-powered coding assistant with a CLI, VS Code/JetBrains integrations, web and desktop surfaces, and an Agent SDK.

**Changes since talk:** The overview page does not mention "dreaming" or managed agents with dreaming capability. The product surface has expanded considerably: remote control, computer use (preview), Slack integration, Chrome extension (beta), scheduled prompts, hooks, and a full Agent SDK are now documented. The talk framed Claude Code as the deployment context for memory and dreaming; the current docs frame it as a general-purpose coding assistant with extensible agent infrastructure.

**Key details for chapter:**
- Claude Code exposes an Agent SDK, relevant to the chapter's multi-agent memory architecture claims.
- Sessions are explicitly documented as starting with a fresh context window; the memory system described in the talk is the documented solution to this limitation.
- Installation is now via `curl -fsSL https://claude.ai/install.sh | bash` (native) or Homebrew/WinGet; chapter should reference current install paths if it mentions setup.

---

## MCP / Model Context Protocol

**Current status:** The URL `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404 Not Found. The MCP documentation has moved.

**Changes since talk:** The page at the linked URL no longer exists. Based on training data and the Claude Code docs sidebar (which lists "Model Context Protocol (MCP)" under "Tools and plugins" in the Claude Code docs), MCP documentation has been reorganized into the Claude Code docs rather than living under `agents-and-tools`. The canonical MCP specification now lives at `modelcontextprotocol.io`. The talk references MCP as the tool layer through which agents access file-system memory; this architecture is consistent with what MCP does, but verify the current doc URL before citing.

**Key details for chapter:**
- Cite `https://code.claude.com/docs` or `modelcontextprotocol.io` for MCP references; the `agents-and-tools` path is broken.
- MCP appears in the Claude Code sidebar under "Tools and plugins," suggesting it is now primarily documented as a Claude Code extension mechanism rather than a standalone API concept.
- The talk's claim that memory is accessed via "familiar tools like Bash and grep" is consistent with MCP's tool-call model, but the chapter should clarify whether it means MCP-exposed tools or native shell access.

---

## context window

**Current status:** Opus 4.7 and Sonnet 4.6 support 1M token context windows; Haiku 4.5 supports 200k tokens.

**Changes since talk:** Context windows have grown. At most plausible talk dates, Sonnet-class models had 200k context windows. The 1M token window for Opus and Sonnet is a material change relevant to how much session history a dreaming process can ingest in a single call.

**Key details for chapter:**
- 1M token context window for Opus 4.7 and Sonnet 4.6 means a single dreaming pass can analyze substantially more session transcript than was possible at talk time.
- Haiku 4.5 remains at 200k tokens; if the chapter discusses cost-optimized dreaming using smaller models, this limit applies.
- Max output is 128k tokens for Opus 4.7 and 64k for Sonnet 4.6 and Haiku 4.5; relevant if dreaming produces reorganized memory documents as output.

---

## memory

**Current status:** Claude Code memory consists of two systems: CLAUDE.md files (human-authored persistent instructions) and auto memory (notes Claude writes itself from corrections and preferences), both loaded at session start.

**Changes since talk:** The talk describes a more expansive enterprise memory architecture with hierarchical scopes, optimistic concurrency control, version control, audit trails, and a standalone API. The current Claude Code memory docs describe a simpler two-mechanism system scoped to individual users and projects, with no mention of multi-agent shared memory stores, dreaming, org-level memory hierarchies, or enterprise concurrency controls. Either these features are in a separate enterprise or managed-agent product not covered by this doc page, or they postdate the docs snapshot, or they remain in preview and are not yet in the public Claude Code docs. The chapter should not imply the full enterprise architecture is in the Claude Code memory page linked.

**Key details for chapter:**
- The documented memory mechanism uses `CLAUDE.md` files at multiple directory scopes (global `~/.claude/CLAUDE.md`, project root, subdirectory) to create a rough hierarchy, consistent with the talk's scope concept.
- Auto memory is the closest documented analog to the talk's "learning from sessions" concept: Claude writes notes based on user corrections and preferences without explicit instruction.
- The `CLAUDE.md` vs auto memory distinction maps loosely onto the talk's read-only org memory vs read-write task memory framing, though the docs do not use those terms.

---

## skills

**Current status:** Skills are SKILL.md files placed at `.claude/skills/<name>/SKILL.md` that extend Claude's capabilities; they load only when invoked, via `/skill-name` or automatic relevance matching.

**Changes since talk:** The skills page represents a distinct Claude Code extensibility primitive not explicitly named in the talk. Notably, the docs state: "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way." This consolidation happened after earlier Claude Code releases. The talk does not mention skills by name; the entity was listed for enrichment presumably because skills are the mechanism by which procedural knowledge can be persisted across sessions, which is adjacent to the memory topic.

**Key details for chapter:**
- Skills are lazy-loaded (body loads only when invoked), making them a low-overhead way to store procedural memory that complements CLAUDE.md fact-based memory.
- The `/skill-name` invocation pattern means skills function as named, reusable procedures, analogous to the "organizational knowledge" the talk describes dreaming as curating.
- Skills and CLAUDE.md together form Claude Code's current published memory surface; the talk's enterprise features (concurrency, audit, API) are not represented here.

---

## Improvement opportunities

- **Diagram: memory hierarchy and scope.** A layered diagram showing org-level read-only memory, project-level shared memory, and session-level read-write memory stores, with arrows indicating which agents can read or write each layer. Should show optimistic concurrency control as a label on the shared-write boundary. Maps directly to the talk's multi-agent memory architecture claim.

- **Diagram: dreaming pipeline flow.** A sequence or pipeline diagram showing: agent sessions produce transcripts, transcripts are batched, dreaming process runs out-of-band, optimized memory is written back to shared store, subsequent agents read improved memory. Emphasize the decoupling from the agent loop, which the speaker called "really, really critical."

- **Comparison table: in-band vs out-of-band memory optimization.** Two-column table contrasting what happens if memory is updated synchronously during agent execution (latency impact, limited cross-session visibility, no global pattern detection) versus asynchronously via dreaming (no latency, cross-agent pattern detection, deduplication, quality curation). Grounds the architectural decision in concrete tradeoffs.

- **Comparison table: CLAUDE.md / auto memory / skills / dreaming.** Four-row table mapping each mechanism to: who writes it (human / agent / dreaming process), when it loads (always / always / on-invoke / batch), scope (user/project / session / project / org), and primary use case. Helps readers orient among the overlapping persistence mechanisms.

- **Code example: CLAUDE.md structure for hierarchical memory.** A minimal example showing `~/.claude/CLAUDE.md` (org-level facts), `./CLAUDE.md` (project-level conventions), and a subdirectory-scoped `CLAUDE.md`, with annotations on which content belongs at each level. Illustrates the file system memory model the talk describes using current documented primitives.

- **Code example: skill file for a recurring procedure.** A `.claude/skills/code-review/SKILL.md` example showing the format for a multi-step procedure (e.g., a legal document review checklist, loosely analogous to Harvey's use case), with the invocation pattern `/code-review`. Demonstrates how skills operationalize the "curated organizational knowledge" concept from the dreaming section.

- **Worked example: dreaming improving a shared memory store.** A before/after scenario: five agents each independently discover that a codebase uses a non-standard import convention and each writes a slightly different note about it. Dreaming consolidates these into one canonical rule, deduplicates, and writes it to org memory. Subsequent agents start with the clean rule. Concretizes the "97% decrease in first-pass errors" claim with a mechanistic explanation.

- **Callout: dreaming availability status.** The talk explicitly states dreaming is in "Research Preview" and works with "managed agents." The current Claude Code public docs do not document dreaming. The chapter should include a dated note clarifying the feature's availability status at talk time and directing readers to check current managed agent or enterprise documentation, since the public docs snapshot does not cover it.
