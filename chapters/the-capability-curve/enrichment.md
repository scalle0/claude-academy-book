# Enrichment notes: The capability curve

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 2/2

---

## Claude

**Current status:** The current flagship model is Claude Opus 4.7, with the model lineup now spanning the Claude 4.x generation (Opus 4.7, Sonnet 4.6, Haiku 4.5).

**Changes since talk:** The talk referenced Claude Sonnet 3.7 and SweeBench performance at 87%. The model lineup has advanced substantially: Claude 3.7 Sonnet is now a legacy model, and the current generation is Claude 4.x. The naming convention has also changed starting with the 4.6 generation, where model IDs no longer include date stamps (e.g., `claude-opus-4-7` rather than `claude-opus-4-7-20250929`). Claude Opus 4.7 is described as offering "a step-change improvement in agentic coding over Claude Opus 4.6," which aligns with the trajectory the talk was describing.

**Key details for chapter:**
- Current recommended model for complex agentic coding tasks is Claude Opus 4.7 (`claude-opus-4-7`); Sonnet 3.7, referenced in the talk's live demo comparison, is now a legacy model.
- The "adaptive thinking" feature mentioned in the docs (available on Opus 4.7 and Sonnet 4.6, not Haiku 4.5) maps to the talk's claim about models performing autonomous planning and reasoning before acting, though the specific terminology has evolved.
- Pricing for the current frontier model is $5/MTok input, $25/MTok output for Opus 4.7; this context is useful for cost-framing any discussion of long agentic runs.

---

## Claude Code

**Current status:** Claude Code is a production AI coding assistant available as a terminal CLI, VS Code extension, JetBrains plugin, web interface, and desktop app, with support for third-party providers in some surfaces.

**Changes since talk:** At talk time, Claude Code was positioned as a newer agentic coding tool. It has since expanded significantly: it now has dedicated documentation at `code.claude.com`, an Agent SDK, remote control capabilities, a Chrome extension (beta), computer use (preview), Slack integration, and CI/CD integrations. The surface area has grown from primarily a CLI tool to a multi-platform product. Claude Code on the web and desktop app are now available surfaces that did not exist or were not prominent at talk time.

**Key details for chapter:**
- Claude Code is available via `curl -fsSL https://claude.ai/install.sh | bash` (native install) as well as Homebrew, WinGet, and platform-specific installers; this is the canonical install path.
- The product now has a dedicated Agent SDK, which is relevant to the talk's discussion of building autonomous agents and scaffolding; teams building the kind of long-running agents described in the Bun rewrite example now have a first-party SDK rather than relying on custom scaffolding.
- The "Explore the context window" documentation section exists as a named concept in the Claude Code docs, reinforcing the talk's point about long-horizon coherence as a first-class concern.

---

## context window

**Current status:** Current Claude models offer either 1M token context windows (Opus 4.7, Sonnet 4.6) or 200k tokens (Haiku 4.5), with max output of 128k tokens (Opus 4.7) or 64k tokens (Sonnet 4.6, Haiku 4.5).

**Changes since talk:** The talk discussed long-horizon coherence across "millions of tokens" as an emerging capability. The 1M token context window is now a production spec for two of the three current models, not an experimental ceiling. The Claude Code docs also include a dedicated "Explore the context window" page, indicating that context management is now a documented operational concern rather than a research topic. The Max output limits are also worth noting: the Message Batches API supports up to 300k output tokens for Opus 4.7, Opus 4.6, and Sonnet 4.6 using the `output-300k-2026-03-24` beta header.

**Key details for chapter:**
- Opus 4.7 and Sonnet 4.6 both have 1M token context windows; this is now standard for frontier models, not a differentiating feature.
- The `output-300k-2026-03-24` beta header on the Message Batches API enables up to 300k output tokens, which is directly relevant for the kind of long autonomous runs (multi-hour, large codebase rewrites) the talk described.
- Context window size can be queried programmatically via the Models API, which returns `max_input_tokens`, `max_tokens`, and a `capabilities` object per model.

---

## Improvement opportunities

- **Comparison table: Model capability progression.** A table showing SweeBench-style benchmark scores alongside model generation (3.5, 3.7, 4.x) and context window size would make the "capability curve" concrete. Should include: model name, release approximate date, SweeBench score if available, context window, and a qualitative tier (junior/senior engineer analogy from the talk).

- **Diagram: Agentic loop architecture.** A flowchart showing the planning, execution, error detection, and recovery cycle described in the talk, annotated with where the capability improvements occur (planning before acting, error recovery, long-horizon coherence). Should contrast the "doom loop" failure mode against the adaptive recovery behavior now standard in frontier models.

- **Code example: Long-running agent with closed-loop error recovery.** A minimal Claude Code API call or Agent SDK snippet showing a multi-step task with error handling, illustrating the difference between a scaffolded-planning approach (forcing a plan via system prompt) versus letting the model plan autonomously. Should use `claude-opus-4-7` and demonstrate the `output-300k-2026-03-24` beta header on the Batches API for large output tasks.

- **Comparison table: Scaffolding requirements over model generations.** Side-by-side showing what a developer had to put in a system prompt or wrapper script for Claude 3.5 versus what can be omitted with Claude 4.x. Columns: behavior (planning, error recovery, tool use), required in 3.5 era, required in 4.x era. Directly addresses the talk's advice to shrink scaffolding as models improve.

- **Worked example: Evaluation framework for agentic coding tasks.** A concrete eval structure treating coding agent tasks as unit tests, mapping to the talk's claim that "evaluations are just unit tests and regression tests." Should show: task specification, pass/fail criteria, and how to measure real use-case fidelity rather than benchmark proxies. Reference the SweeBench saturation problem as motivation.

- **Diagram: Context window utilization in a long-horizon agent run.** A timeline diagram of a multi-hour agent run (inspired by the Bun rewrite example) showing token consumption across planning, execution, and recovery phases. Annotates where context pressure occurs and how the 1M token window enables sustained attention across a full codebase rewrite.

- **Code example: Claude Code install and first agentic task via CLI.** The canonical install one-liner (`curl -fsSL https://claude.ai/install.sh | bash`) followed by a minimal example of invoking Claude Code on a codebase-scale task from the terminal. Should include flags or configuration relevant to autonomous operation (non-interactive mode, permission settings) as documented in the current Claude Code overview.
