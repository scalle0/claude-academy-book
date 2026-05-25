# Enrichment notes: Picking the right model

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 5
Pages fetched: 5/5

---

## Claude

**Current status:** The current flagship generally available model is Claude Opus 4.7, with the active model lineup being Opus 4.7, Sonnet 4.6, and Haiku 4.5.

**Changes since talk:** The model lineup has changed substantially. The talk likely referenced Claude 3.x or early Claude 4 models (Sonnet 4.5, Haiku 3.5, etc.). Current models are Opus 4.7 (`claude-opus-4-7`), Sonnet 4.6 (`claude-sonnet-4-6`), and Haiku 4.5 (`claude-haiku-4-5-20251001`). Pricing has shifted: Opus 4.7 is $5/$25 per MTok input/output, Sonnet 4.6 is $3/$15, Haiku 4.5 is $1/$5. Starting with the 4.6 generation, model IDs use a dateless format that is a pinned snapshot, not an evergreen pointer. Context windows are now 1M tokens for Opus and Sonnet, 200k for Haiku.

**Key details for chapter:**
- Current recommended starting point is Claude Opus 4.7 for complex/agentic tasks; Sonnet 4.6 for speed/intelligence balance; Haiku 4.5 for fastest responses
- Every model ID is a pinned snapshot; aliases like `claude-sonnet-4-6` resolve to a fixed release, not a rolling update (behavior that burned teams doing model-version comparisons)
- The talk's point about behavior varying between model versions is confirmed by the docs, which explicitly call out migration guidance when moving between major versions

---

## Claude Code

**Current status:** Claude Code is a full-featured agentic coding assistant available as a CLI, VS Code extension, desktop app, web interface, and JetBrains plugin.

**Changes since talk:** The talk references Claude Code as an entity worth enriching but does not appear to discuss it substantively in the summary or quotes. The current docs show Claude Code has expanded significantly: it now supports remote control, computer use (preview), Chrome extension (beta), Slack integration, and an Agent SDK. It supports third-party providers in the Terminal CLI and VS Code surfaces. The overview page has moved to `code.claude.com/docs` with a separate docs site.

**Key details for chapter:**
- Claude Code is available via `curl -fsSL https://claude.ai/install.sh | bash` for macOS/Linux/WSL; it requires a Claude subscription or Anthropic Console account on most surfaces
- Claude Opus 4.7 documentation specifically calls out "a step-change improvement in agentic coding" as the primary migration reason from Opus 4.6, making it directly relevant to the talk's model-selection framework
- If the chapter discusses using Claude Code for running evals or agentic benchmarks (like TauBench), note that Claude Code has a prompt caching integration documented at the Claude Code overview level

---

## MCP

**Current status:** The URL `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404; the page has moved or been reorganized.

**Changes since talk:** The fetch returned a Not Found page. Based on training data: MCP (Model Context Protocol) is Anthropic's open protocol for connecting AI models to external data sources and tools. It has seen significant adoption and ecosystem growth. The current docs sidebar shows MCP is now under a dedicated "MCP" section with subsections for Remote MCP servers, MCP connector, and MCP tunnels, suggesting the architecture has matured beyond the single-page overview that likely existed at talk time. The current canonical MCP documentation appears to have moved; check `https://docs.anthropic.com/en/docs/mcp` or the MCP-specific sidebar entries.

**Key details for chapter:**
- The talk's "hot take" quote directly argues against over-investing in complex multi-agent orchestration (which MCP enables) in favor of context hygiene; this is a defensible position worth noting as a design tradeoff, not a dismissal of MCP
- MCP is now a stable, open standard with broad third-party support; the chapter should distinguish between "MCP as infrastructure" (connecting tools to models) and "multi-agent orchestration complexity" (the target of the speaker's criticism)
- Cannot provide authoritative current MCP API details from the fetched page; verify current server configuration format at the updated docs URL before including code examples

---

## prompt caching

**Current status:** Prompt caching supports both automatic top-level caching and explicit block-level cache breakpoints, with 5-minute (default) and 1-hour TTL options, at 0.1x base input token price for cache hits.

**Changes since talk:** The talk states cache hits cost "one tenth the price of the list price of input tokens," which matches the current 0.1x multiplier. However, several features are new since a typical 2024 talk date: (1) automatic caching via a top-level `cache_control` field is a new mode that did not require explicit block-level markers, (2) 1-hour TTL is now available at 2x base input price (vs. only 5-minute TTL previously), (3) cache diagnostics is now a beta feature, (4) the minimum token threshold requirement still exists but the docs no longer prominently feature it. The 5-minute default TTL and 0.1x cache read price are unchanged.

**Key details for chapter:**
- Cache hit price is 0.1x base input tokens (confirmed); cache write price is 1.25x base input tokens for 5-minute TTL, 2x for 1-hour TTL. The talk's "one tenth" figure is accurate for reads but the chapter should note write overhead
- Automatic caching (new): add `cache_control: {"type": "ephemeral"}` at the request top level; the system automatically moves the cache breakpoint forward as conversations grow, eliminating manual marker management for multi-turn use cases
- Prompt caching now supports all active Claude models; the chapter should not imply it is limited to specific tiers

---

## thinking

**Current status:** Extended thinking has been substantially restructured: Claude Opus 4.7 requires adaptive thinking (`thinking: {type: "adaptive"}`) with the `effort` parameter; manual `budget_tokens` mode returns a 400 error on Opus 4.7 and is deprecated on Opus 4.6 and Sonnet 4.6.

**Changes since talk:** This is a significant breaking change relative to talk-era content. The original extended thinking API used `thinking: {type: "enabled", budget_tokens: N}` to set an explicit token budget. On current Claude Opus 4.7, this call fails with a 400 error. The replacement is adaptive thinking with an `effort` parameter. Additionally: (1) summarized thinking is now the default on Claude 4 models (full thinking not returned by default), (2) a `display` field controls whether thinking is `"summarized"` or `"omitted"` in responses, (3) omitted thinking reduces latency but not cost since full thinking tokens are still charged, (4) Claude Haiku 4.5 does not support extended thinking.

**Key details for chapter:**
- Any code example using `budget_tokens` must be flagged as deprecated or updated; on Opus 4.7 it causes a hard 400 error, not degraded behavior
- The talk's discussion of "thinking modes" and "effort levels" as cost-accuracy levers maps to the current `effort` parameter in adaptive thinking; the concept is valid but the implementation API has changed
- Thinking tokens are billed at full cost even when `display: "omitted"` is set; the chapter's cost modeling for thinking-enabled workloads must account for this

---

## Improvement opportunities

- **Comparison table: model selection decision matrix.** The talk's core thesis is cost-per-successful-outcome rather than cost-per-token. A table with columns for Model, Input $/MTok, Output $/MTok, Cache Hit $/MTok, Context Window, Extended Thinking Support, and Relative Task Success Rate (from eval) would operationalize this directly. Include current Opus 4.7 / Sonnet 4.6 / Haiku 4.5 pricing from the docs.

- **Code example: prompt caching with cache hit rate measurement.** The talk claims 80-90% cache hit rates are achievable. Show a Python snippet using the current automatic caching API (`cache_control` at request top level) that logs `response.usage.cache_read_input_tokens` vs `response.usage.input_tokens` to compute observed hit rate. This directly validates the speaker's claim in production.

- **Code example: adaptive thinking with effort parameter.** The talk discusses using "thinking modes" and "effort levels" as cost-accuracy levers. Provide a Python snippet showing the current Opus 4.7 API call with `thinking: {"type": "adaptive"}` and `effort` parameter variants (low/medium/high), since the `budget_tokens` approach shown in older talks now returns a 400 on the current flagship model.

- **Worked example: context engineering token reduction.** The talk claims 65-77% token reduction from context hygiene. Show a before/after example with a verbose tool response and a cleaned version, with `anthropic.client.messages.count_tokens()` calls on both to produce a concrete number. This makes the "compounds every time" claim quantitative.

- **Diagram: cost-accuracy frontier.** A 2D scatter plot concept (accuracy on Y axis, cost-per-1000-calls on X axis) with labeled points for each model/configuration combination tested in the TauBench workshop: Haiku with no thinking, Sonnet with no thinking, Sonnet with adaptive thinking, Opus with adaptive thinking. Illustrates the counterintuitive finding that higher-intelligence models can dominate on both axes simultaneously.

- **Diagram: prompt caching cache hit flow.** A sequence diagram showing two API requests: Request 1 (cache miss, full processing, cache write) and Request 2 (cache hit, partial processing). Label the token counts and costs at each step using current pricing multipliers (1.25x write, 0.1x read). The talk explains this verbally; a visual would clarify the prefix-matching mechanics.

- **Comparison table: eval pitfall taxonomy.** The talk identifies three named failure modes: noise vs. signal confusion, infrastructure failures, and silent saturation. A table with columns for Pitfall Name, Symptom, Detection Method, and Mitigation would make this actionable. Include the "Claude reading Git history" example from the transcript under silent saturation.

- **Worked example: TauBench eval setup.** The talk demonstrates running evals across multiple models. A minimal reproducible example showing how to run TauBench against two model configurations, collect per-task success rates, and compute cost-per-successful-outcome using actual API usage metadata (`input_tokens`, `output_tokens`, `cache_read_input_tokens`) would anchor the talk's methodology in runnable code.
