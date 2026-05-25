# Enrichment notes: The thinking lever

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 4
Pages fetched: 4/4

---

## Claude Code

**Current status:** Claude Code is an agentic coding tool available as a CLI, VS Code extension, JetBrains plugin, desktop app, and web interface, supporting terminal workflows and full codebase context.

**Changes since talk:** No significant changes to core functionality. The surface area has expanded: the web interface, desktop app, Chrome extension (beta), computer use (preview), and Slack integration are all listed in current docs. The install method is now a curl script (`curl -fsSL https://claude.ai/install.sh | bash`) rather than npm-only. Third-party provider support for CLI and VS Code is now documented. None of these would contradict claims made in the talk.

**Key details for chapter:**
- Claude Code operates across terminal, VS Code, JetBrains, desktop, and web surfaces; all require a Claude subscription or Anthropic Console account except CLI and VS Code which also support third-party providers.
- The tool is positioned as understanding "your entire codebase" and working "across multiple files and tools," which aligns with the talk's framing of agentic coding as a benchmark domain for test time compute gains.
- Full documentation index is available at `https://code.claude.com/docs/llms.txt`.

---

## MCP

**Current status:** The MCP page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404/Not Found response.

**Changes since talk:** Cannot verify from fetched docs. From training data: MCP (Model Context Protocol) is an open protocol for connecting Claude to external tools and data sources via a standardized server/client interface. The current docs sidebar (visible in the extended thinking page fetch) shows MCP is now organized under two sub-pages: "Remote MCP servers" and "MCP connector," with a note in the tool use overview directing users to `modelcontextprotocol.io` for building custom MCP clients. This suggests MCP documentation has been restructured since the talk, with the top-level overview page either moved or replaced by more specific sub-pages. Treat claims about MCP doc structure with a caveat until the page is re-fetched.

**Key details for chapter:**
- The canonical external reference for MCP client development is now `modelcontextprotocol.io`; the Anthropic docs focus on remote MCP servers and the MCP connector specifically.
- The tool use overview explicitly distinguishes the MCP connector (for connecting to MCP servers) from building your own MCP client, indicating a clearer separation of concerns than may have existed at talk time.
- The MCP page structure change (from a single overview to remote-servers + connector sub-pages) may reflect maturation of the protocol and a shift toward hosted/remote server patterns.

---

## thinking

**Current status:** Extended thinking provides Claude with a scratchpad reasoning process before its final response; the current docs distinguish between manual extended thinking (`type: "enabled"`, `budget_tokens`) and adaptive thinking (`type: "adaptive"`) with the effort parameter, with manual mode deprecated on newer models.

**Changes since talk:** Significant changes. The talk describes adaptive thinking as an "evolution of interleaved thinking" that was current or near-current at recording time. Since then:

- Manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) is **no longer supported on Claude Opus 4.7** and returns a 400 error on that model.
- Claude Mythos Preview is now documented; it uses adaptive thinking as default, does not support `thinking: {type: "disabled"}`, and defaults `display` to `"omitted"` rather than returning thinking content.
- Summarized thinking is now the default return format for Claude 4 models. Full thinking output requires contacting Anthropic sales.
- A `display` field now controls whether thinking blocks are returned as `"summarized"` or `"omitted"`. The `"omitted"` option reduces latency without reducing cost.
- The `budget_tokens` parameter is deprecated on Claude Opus 4.6 and Claude Sonnet 4.6.
- Output token limits: Claude Mythos Preview, Opus 4.7, and Opus 4.6 support up to 128k output tokens; Sonnet 4.6 and Haiku 4.5 support up to 64k. A Message Batches API beta header raises the limit to 300k for select models.

**Key details for chapter:**
- The talk's framing of thinking as a "toggle" is now technically obsolete for current models: the correct API surface is `thinking: {type: "adaptive"}` with an `effort` parameter, not a binary enable/disable. The talk's argument that a toggle is a poor proxy maps directly onto why the current API moved away from it.
- Summarized thinking is the default; users are billed for full thinking tokens regardless of what is returned in the response, which is a non-obvious cost consideration.
- The `display: "omitted"` option is relevant to the talk's latency discussion: omitting thinking blocks reduces time-to-first-text-token without changing the model's reasoning depth or cost.

---

## tool use

**Current status:** Tool use lets Claude call client-defined functions or Anthropic-provided server tools; client tools execute in the caller's application while server tools (web search, code execution, web fetch, tool search) execute on Anthropic infrastructure.

**Changes since talk:** The client/server tool distinction is now more explicit and documented with its own taxonomy. Server tools listed in current docs include: `web_search`, `code_execution`, `web_fetch`, and `tool_search`. New Anthropic-provided tools now documented: Advisor tool, Memory tool, Bash tool, Computer use tool, Text editor tool. A `strict: true` parameter for schema conformance (strict tool use) is now available. Tool Runner (SDK) and fine-grained tool streaming are new. Pricing table now covers Claude Opus 4.7, Opus 4.6, Opus 4.5, Opus 4.1, Sonnet 4.6, Sonnet 4.5, Haiku 4.5, and several deprecated/retired models.

**Key details for chapter:**
- The talk's analogy ("we give Claude a search tool and allow it to reason as to when it should search") now has a literal implementation: `web_search_20260209` is a server tool where Anthropic handles execution, and Claude decides autonomously whether to call it. This is a direct concrete instance of the capability-not-toggle philosophy.
- Tool access produces "outsized capability gains" on benchmarks including LAB-Bench FigQA and SWE-bench, per current docs, corroborating the talk's test time compute claims with specific benchmark names.
- The system prompt overhead for tool use is 346 tokens (`auto`/`none` tool choice) or 313 tokens (`any`/`tool` choice) for current Claude 4 models; this is relevant to the token budget discussion in the talk.

---

## Improvement opportunities

- **Comparison table: thinking configuration by model.** The talk discusses effort levels and budget controls without specifying which API surface maps to which model. A table with columns for model name, supported `thinking.type` values, `effort` parameter support, `display` options, and max output tokens would let readers quickly determine the correct configuration for their target model. Draw from the current extended thinking docs.

- **Code example: adaptive thinking with effort parameter.** The talk argues thinking should be a default capability, not a toggle. Show a minimal Messages API call using `thinking: {type: "adaptive"}` with `effort: "high"` versus `effort: "low"`, including how the response's thinking block differs. Contrast this with the now-deprecated `budget_tokens` pattern to make the API evolution concrete.

- **Diagram: test time compute mechanisms.** The talk identifies three primary mechanisms: thinking (scratchpad), tool calling (external interaction), and text output. A flow diagram showing a single inference pass with branching paths for each mechanism, labeled with where tokens are consumed and where latency is introduced, would make the architecture legible. Include the adaptive decision point where Claude chooses whether to think at all.

- **Comparison table: interleaved thinking vs. adaptive thinking.** The talk explicitly contrasts these two approaches. A side-by-side table covering: control model (predetermined vs. autonomous), when thinking occurs, whether the model can skip thinking, API parameter used, and deprecation status would clarify the distinction the talk is arguing for.

- **Worked example: effort level tradeoffs on a coding task.** The talk claims extra high effort provides optimal Pareto efficiency and that low effort can produce novel approaches through constraint. Show a single coding problem (e.g., a SWE-bench-style bug fix) run at `effort: "low"`, `effort: "high"`, and `effort: "max"`, with token counts and latency for each. Quantify the diminishing returns the talk describes.

- **Code example: tool use with web search as capability-not-toggle.** The talk's clearest analogy is web search: "we give Claude a search tool and allow it to reason as to when it should search." Show a Messages API call with `web_search_20260209` as a server tool, alongside the response showing whether Claude chose to invoke it, to make the capability-provision pattern concrete and tie it back to the thinking-as-tool argument.

- **Diagram: performance vs. token expenditure curve.** The talk claims logarithmic scaling of performance with tokens across knowledge domains. A chart with token budget on the x-axis and benchmark score on the y-axis, with separate curves for reasoning, computer use, and PhD-level exams, would anchor the logarithmic claim visually. Mark the "extra high effort" Pareto-optimal point explicitly.
