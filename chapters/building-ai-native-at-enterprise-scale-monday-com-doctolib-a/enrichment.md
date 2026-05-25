# Enrichment notes: Building AI-native at enterprise scale: monday.com, Doctolib, and Delivery Hero

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 2
Pages fetched: 2/2

---

## Claude

**Current status:** Claude's current generally available model lineup is Claude Opus 4.7 (most capable, agentic coding), Claude Sonnet 4.6 (balanced speed/intelligence), and Claude Haiku 4.5 (fastest), all with 1M token context windows except Haiku 4.5 (200k).

**Changes since talk:** The model family has advanced substantially. The talk predates the Claude 4.x generation. At recording time, the speakers would have been evaluating and deploying Claude 3.x models (likely Sonnet/Opus 3.x variants). The current lineup uses a dateless versioning format starting with Claude 4.6+, where model IDs are pinned snapshots rather than evergreen pointers. Claude Opus 4.7 is highlighted specifically for "a step-change improvement in agentic coding," directly relevant to what all three companies are building. Extended thinking is available on Sonnet 4.6 and Haiku 4.5 but not Opus 4.7; adaptive thinking is available on Opus 4.7 and Sonnet 4.6.

**Key details for chapter:**

- The versioning behavior the speakers describe ("treat it as a completely different thing") is now formally reflected in Anthropic's own documentation: every model ID is a pinned snapshot, and starting with 4.6, even dateless IDs are fixed, not evergreen pointers. This validates the panel's migration advice at an architectural level.
- For agentic workloads like Delivery Hero's HeroGen council-of-agents pattern, Claude Opus 4.7 is the current recommended entry point; the Models API allows programmatic capability and token-limit queries, which is useful for systems that dynamically select models.
- Pricing as of current docs: Opus 4.7 at $5/$25 per MTok (input/output), Sonnet 4.6 at $3/$15, Haiku 4.5 at $1/$5. Multi-model council architectures (as described by Delivery Hero) carry meaningful per-token cost implications that must be factored into system design.

---

## Claude Code

**Current status:** Claude Code is a generally available AI-powered coding assistant, offered as a terminal CLI, VS Code extension, JetBrains plugin, desktop app, and web surface, with support for third-party providers in the CLI and VS Code.

**Changes since talk:** At recording time, Claude Code was a newer or less mature product; the speakers were describing agent orchestration patterns they built themselves (HeroGen, Vibe, skills marketplace) rather than referencing Claude Code as an off-the-shelf tool. Claude Code is now a full product with its own documentation site (code.claude.com), an Agent SDK, remote control capability, CI/CD integration, Slack integration, and a Chrome extension in beta. The "council of agents" pattern Delivery Hero describes is now expressible using Claude Code's native multi-agent and orchestration primitives rather than requiring fully custom infrastructure.

**Key details for chapter:**

- Claude Code supports installation via curl on macOS/Linux/WSL (`curl -fsSL https://claude.ai/install.sh | bash`) and WinGet on Windows, making it straightforward to deploy in enterprise CI/CD pipelines of the type Delivery Hero describes.
- The Agent SDK (listed in current docs navigation) provides building blocks for the kind of orchestration all three companies implemented ad hoc; chapters discussing custom agent frameworks should note this as the current preferred starting point.
- Claude Code integrates with code review and CI/CD natively, which directly addresses the pull-request-centric success metric (merge rate, 85% PR success) that Delivery Hero uses as its primary KPI.

---

## Improvement opportunities

- **Council-of-agents diagram:** Architectural diagram showing Delivery Hero's HeroGen pattern: a primary code-generation agent submitting a PR, then multiple review-model instances evaluating the same diff in parallel, with a consensus or threshold gate before merge. Should include model selection at each node and the feedback loop for failed PRs.

- **Model selection comparison table:** Side-by-side table of Claude Opus 4.7, Sonnet 4.6, and Haiku 4.5 covering: context window, max output, pricing, extended/adaptive thinking availability, and recommended use case in an agentic pipeline. This directly supports the panel's advice that model upgrades require full re-evaluation, not a drop-in swap.

- **Agent identity code example:** Snippet showing how to register an agent as a first-class principal in an API-first identity system, specifically an API call that uses a service account or machine identity (not a human SSO token) to authenticate a Claude API request. Should contrast with naive human-user-token reuse and show the recommended `x-api-key` or OAuth client-credentials pattern.

- **Skills marketplace schema example:** JSON or YAML structure defining a "skill" entry as it might appear in Doctolib's marketplace: skill name, owning team, Claude model pinned version, system prompt location, usage count field, and discovery tags. Illustrates how standardized metadata enables the "which skills are trending" visibility the speaker describes.

- **PR success rate instrumentation example:** Python or shell pseudocode showing how Delivery Hero's 85% metric is computed: emit a structured log event on PR open (agent-generated flag), on PR merge, on PR close-without-merge, then a simple aggregation query. Grounds the abstract metric claim in a concrete observability pattern.

- **Model migration checklist:** Ordered list of steps derived from the panel's "treat it as a completely different system" advice, covering: snapshot the current model ID (do not use an alias), run the full eval suite against the new model ID before any traffic shift, compare output distributions not just pass/fail rates, update system prompts independently, and document behavioral deltas. Should reference Anthropic's current pinned-snapshot versioning behavior as the mechanism that makes controlled migration possible.

- **Monolith-vs-modular codebase comparison table:** Two-column table contrasting AI agent integration characteristics: file count per feature, average function length, API surface discoverability, context-window fit, test harness availability, and observed agent task success rate. Derived from the panel's claim that smaller standardized codebases "significantly outperform monolithic systems," this gives readers a diagnostic rubric for their own environments.
