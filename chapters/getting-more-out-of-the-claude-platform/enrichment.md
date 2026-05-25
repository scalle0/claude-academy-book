# Enrichment notes: Getting more out of the Claude Platform

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 5
Pages fetched: 4/5

---

## Claude Code

**Current status:** Claude Code is a multi-surface AI coding assistant (terminal CLI, VS Code, desktop app, web, JetBrains) available via Claude subscription or Anthropic Console account, installable via curl, Homebrew, or WinGet.

**Changes since talk:** The product surface has expanded significantly. Claude Code now ships as a desktop app, web interface, Chrome extension (beta), and computer use (preview) integration, beyond the terminal CLI that was likely the primary surface at talk time. The Agent SDK is now documented as a separate section. Code review and CI/CD integration and Slack integration are listed as platform targets.

**Key details for chapter:**
- Claude Code is available at `https://code.claude.com/docs/llms.txt` for a complete documentation index, useful for programmatic discovery
- Supported installation methods: `curl -fsSL https://claude.ai/install.sh | bash` (macOS/Linux/WSL), Homebrew, WinGet (Windows)
- Third-party provider support is available on Terminal CLI and VS Code surfaces, not all surfaces

---

## MCP

**Current status:** The MCP page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404; the current MCP documentation lives under the prompt caching page's left-nav references as "Remote MCP servers," "MCP connector," and "MCP tunnels" under a dedicated MCP section.

**Changes since talk:** The URL structure has changed. The MCP documentation has been reorganized; the path `agents-and-tools/model-context-protocol` no longer resolves. From training data and the prompt caching page's sidebar nav, MCP now has at least three distinct sub-topics: Remote MCP servers, MCP connector, and MCP tunnels. This suggests the protocol has matured beyond a single overview page into a multi-component integration surface. Caveat: full current content of those pages was not fetched.

**Key details for chapter:**
- Verify current MCP documentation URL before citing; the overview page URL used in the talk's source material is a 404
- The sidebar shows MCP is now treated as a peer section alongside "Tools" and "Tool infrastructure," suggesting it has grown in scope since the talk
- MCP tunnels appear as a new sub-topic not likely covered at talk time; the chapter should note this as a post-talk addition if MCP is discussed

---

## Context window

**Current status:** The models overview page documents three current models: Claude Opus 4.7 and Claude Sonnet 4.6 with 1M token context windows, and Claude Haiku 4.5 with a 200k token context window.

**Changes since talk:** Model names and versions have changed substantially. The current generation is Claude 4.x (Opus 4.7, Sonnet 4.6, Haiku 4.5). Context windows have grown: Opus 4.7 and Sonnet 4.6 both support 1M tokens. The pricing structure is also different from what the speaker would have referenced: Opus 4.7 is $5/MTok input, $25/MTok output. Any specific model names or context window sizes cited in the chapter should be updated to current values.

**Key details for chapter:**
- Opus 4.7 and Sonnet 4.6 both have 1M token context windows; Haiku 4.5 has 200k
- Max output tokens are 128k (Opus 4.7) and 64k (Sonnet 4.6 and Haiku 4.5) on the synchronous Messages API; the Batch API supports up to 300k output tokens for Opus 4.7, Opus 4.6, and Sonnet 4.6 via the `output-300k-2026-03-24` beta header
- Model capabilities and token limits are queryable programmatically via the Models API, which returns `max_input_tokens`, `max_tokens`, and a `capabilities` object per model

---

## Prompt caching

**Current status:** Prompt caching supports two modes (automatic caching via a top-level `cache_control` field, and explicit cache breakpoints on individual content blocks), with a 5-minute default TTL and an optional 1-hour TTL at 2x base input token price.

**Changes since talk:** Several additions since a typical talk of this type. Automatic caching is a new mode that did not exist at typical pre-2025 talk dates: it uses a single top-level `cache_control: {"type": "ephemeral"}` field and moves the cache breakpoint forward automatically as conversations grow, removing the need to manually place breakpoints on each turn. The 1-hour cache duration option is also newer, at 2x base input token price. A Cache diagnostics (beta) page now exists in the sidebar. The 90% cost reduction claim from the talk is consistent with current pricing: cache hits are priced at 0.1x base input token price, which is a 90% reduction.

**Key details for chapter:**
- Automatic caching uses `cache_control = {"type": "ephemeral"}` at the top level of the request; for 1-hour TTL use `{"type": "ephemeral", "ttl": "1h"}`
- Explicit breakpoints and automatic caching can be combined; automatic caching consumes one of four available breakpoint slots
- The 90% discount claim is accurate: cache read tokens are priced at 0.1x base input price across all current models; cache write tokens are 1.25x for 5-minute and 2x for 1-hour TTL

---

## Tool search

**Current status:** The tool search page at `https://docs.anthropic.com/en/docs/claude-code/tool-search` could not be fetched.

**Changes since talk:** Cannot confirm current state. From the prompt caching page sidebar, "Tool search" and "Programmatic tool calling" both appear as distinct documented topics under "Tool infrastructure," consistent with the talk's framing of them as separate techniques. The fact that both are present as first-class documented topics suggests the talk's coverage of these features is still accurate in concept. Caveat: specific API details, parameter names, or behavior changes since the talk cannot be confirmed from available fetched content.

**Key details for chapter:**
- Tool search and programmatic tool calling are both under the "Tool infrastructure" section of current docs, not under a general "Tools" section
- The talk's 10% token reduction claim for tool search should be treated as a customer case study data point, not a guaranteed benchmark
- Fetch `https://docs.anthropic.com/en/docs/claude-code/tool-search` directly to verify current parameter names and any behavior changes before finalizing the chapter

---

## Improvement opportunities

- **Prompt caching: code example.** Add a Python snippet showing automatic caching in a multi-turn agent loop: a `client.messages.create()` call with `cache_control={"type": "ephemeral"}` at the top level, followed by parsing `response.usage` to extract `cache_read_input_tokens` and `cache_creation_input_tokens`, so readers can verify their cache hit rate programmatically.

- **Prompt caching: comparison table.** Add a table comparing the two caching modes (automatic vs. explicit breakpoints) on dimensions: configuration complexity, best use case, TTL options, interaction with conversation growth, and breakpoint slot consumption. The talk describes both approaches but never contrasts them structurally.

- **Cache hit rate: worked example.** Add a calculation showing how the 80% and 90% cache hit rate targets translate to actual cost impact at current pricing. For example: a 10,000-token system prompt processed 1,000 times per day at Sonnet 4.6 pricing ($3/MTok base, $0.30/MTok cached), showing monthly cost at 0%, 80%, and 90% hit rates. This makes the "if you remember nothing else, prompt caching" claim concrete.

- **Context engineering: diagram.** Add a flow diagram showing the token lifecycle in a multi-turn agent: what enters the context window each turn, how tool search filters the available tool list before it reaches the model, and where conversation compaction truncates history. This visualizes the "context engineering" concept the talk defines but does not illustrate.

- **Advisor strategy: comparison table.** Add a table comparing the four optimization strategies (prompt caching, tool search, conversation compaction, advisor strategy) on dimensions: implementation effort, applicable cost reduction, primary mechanism, and when to apply. The talk presents these sequentially in a demo but never summarizes them for reference.

- **Cache invalidation: code example.** The speaker calls out timestamps in system prompts as a common cache-busting mistake. Add a before/after code snippet showing a system prompt with `datetime.now()` interpolated (breaks cache) versus a static system prompt with dynamic context passed in the user message (preserves cache).

- **Model selection: updated comparison table.** The talk references cost differences between models (cheaper models for the advisor strategy's junior role, high-intelligence models for oversight). Add a table of current models with input/output pricing, context window, and a one-line characterization of appropriate use case in the advisor strategy pattern, using current Opus 4.7/Sonnet 4.6/Haiku 4.5 data from the models overview page.
