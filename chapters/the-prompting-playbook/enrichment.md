# Enrichment notes: The prompting playbook

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 1
Pages fetched: 1/1

---

## Claude

**Current status:** The current Claude model lineup is organized around three tiers: Opus 4.7 (most capable, complex reasoning and agentic coding), Sonnet 4.6 (speed/intelligence balance), and Haiku 4.5 (fastest, near-frontier intelligence).

**Changes since talk:** The talk references Claude Sonnet and Opus variants, which were current model names at the time. The specific model versions have changed substantially since any 2024-era recording. Notable current details:

- The flagship model is now Claude Opus 4.7, not any 3.x or earlier 4.x variant. The talk's references to "Sonnet" and "Opus" as categories remain valid, but the specific version numbers are outdated.
- "Adaptive thinking" is now a named capability, available on Opus 4.7 and Sonnet 4.6 but not Haiku 4.5. The talk references this concept informally as reasoning or thinking modes; the current docs use "adaptive thinking" as the product term. "Extended thinking" is a separate capability available only on Sonnet 4.6.
- Context windows are now 1M tokens for Opus 4.7 and Sonnet 4.6, and 200k for Haiku 4.5. These are substantially larger than what would have been current at most 2024 recording dates.
- Model ID versioning convention changed starting with Claude 4.6: IDs use a dateless format (e.g., `claude-sonnet-4-6`) that is still a pinned snapshot, not an evergreen pointer. Earlier models used date-suffixed IDs.

**Key details for chapter:**

- Current production model IDs: `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`. Any code examples in the chapter referencing older model strings (e.g., `claude-3-opus-20240229` or similar) should be updated.
- The adaptive thinking capability the talk discusses in the context of "models with reasoning" maps to the current "adaptive thinking" feature on Opus 4.7 and Sonnet 4.6. Haiku 4.5 does not support it.
- Pricing: Opus 4.7 at $5/$25 per MTok input/output; Sonnet 4.6 at $3/$15; Haiku 4.5 at $1/$5. These figures are relevant when the chapter discusses token efficiency trade-offs in agentic vs. monolithic prompting approaches.

---

## Improvement opportunities

- **Comparison table: Model selection for prompting strategies.** The talk compares Sonnet vs. Opus with and without adaptive thinking across a scheduling task. A table with columns for model name, adaptive thinking support, relative cost, latency tier, and recommended use case (monolithic prompt vs. agentic loop) would make the trade-off analysis concrete and updatable.

- **Diagram: Generate-evaluate-repair loop architecture.** A flow chart showing the agentic approach for the staff scheduling example: initial generation step, evaluation step with pass/fail branch, repair step with iteration limit, and final output. Should label where soft constraints are injected at runtime vs. hardcoded in the prompt.

- **Code example: XML-structured system prompt before/after.** A side-by-side showing a flat, unstructured customer support prompt and the same prompt reformatted with XML tags (`<guidelines>`, `<policy>`, `<data>`, `<output_contract>`). Directly illustrates the hygiene principle quote about models not being able to distinguish guidelines from policy from data.

- **Code example: Tool definition for calculation tasks.** An API request body showing a `tools` array with a calculator or lookup tool, paired with a system prompt that removes the instruction "it is critical to calculate X correctly." Illustrates the claim that instructions don't add capability and tools are the correct mechanism.

- **Worked example: Evaluation suite structure.** A concrete test matrix for the telecom customer support bot with three columns: test type (control, edge case, capability boundary), example input, and expected output behavior. Demonstrates how to operationalize the evaluation framework described in the talk.

- **Diagram: Prompt version control with defensive change tracking.** A simple table or changelog format showing prompt version, date, change description, and a "reason/can-revert?" column. Directly implements the advice from the quote about tracking defensive changes so they can be backtracked when migrating models.

- **Comparison table: Monolithic vs. agentic prompting trade-offs.** Rows for: task complexity handling, token usage, debuggability, soft constraint flexibility, failure mode visibility, and model size requirement. Based on the scheduling example analysis, with current Sonnet 4.6 and Opus 4.7 as the reference models.

- **Code example: Soft constraint injection in a multi-step pipeline.** A Python snippet showing a scheduling pipeline where the evaluate step accepts a `soft_constraints` parameter at runtime, demonstrating how multi-step systems allow constraint adjustment without modifying the core evaluation function.
