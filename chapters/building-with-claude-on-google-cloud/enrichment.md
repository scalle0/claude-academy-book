# Enrichment notes: Building with Claude on Google Cloud

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 3/3

---

## Claude Code

**Current status:** Claude Code is a production coding agent available across terminal CLI, VS Code, desktop app, web, and JetBrains, with installation via curl script, Homebrew, or WinGet.

**Changes since talk:** The docs show substantially expanded platform support and distribution options since a 2024-era conference talk. The overview page now documents a full Agent SDK, hooks-based automation, scheduled prompt execution, and external event push to Claude. The sidebar navigation has reorganized under sections including "Agents and parallel work," "Tools and plugins," and "Automation," suggesting significant feature growth beyond what the talk demonstrated. No indication the core value proposition has changed, but the feature surface is considerably larger.

**Key details for chapter:**
- Claude Code installs via `curl -fsSL https://claude.ai/install.sh | bash` on macOS/Linux/WSL; Windows support via WinGet. Third-party providers (including Google Cloud Vertex AI) are supported on Terminal CLI and VS Code surfaces.
- Supports multiple IDE integrations natively: VS Code, JetBrains IDEs, a Chrome extension (beta), and a web surface, plus CI/CD and Slack integrations.
- The docs live at `code.claude.com/docs` with an index at `https://code.claude.com/docs/llms.txt`.

---

## MCP

**Current status:** The URL `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returns a 404/Not Found, so the MCP documentation has moved or been reorganized.

**Changes since talk:** Page fetch failed with Not Found. Based on training data and what the Claude Code sub-agents page reveals, MCP is now documented under Claude Code's own docs site rather than the main Anthropic API docs. The Claude Code sidebar shows MCP under "Tools and plugins" as "Model Context Protocol (MCP)," with adjacent pages for "Discover and install prebuilt plugins," "Create plugins," and "Extend Claude with skills." This represents a significant organizational shift: MCP has moved from a standalone API-level concept to a Claude Code feature set. The current URL is likely `https://code.claude.com/docs/` under the tools/plugins section. The talk's framing of MCP as a general protocol for tools like BigQuery and Looker remains accurate; the positioning has just shifted toward Claude Code as the primary consumer.

**Key details for chapter:**
- MCP is documented within Claude Code's docs under "Tools and plugins," not at the top-level Anthropic API docs path cited in the talk. Link to `https://code.claude.com/docs/llms.txt` for current paths.
- The docs show "Discover and install prebuilt plugins" as a distinct page, suggesting a plugin registry or catalog now exists, which postdates or extends the MCP server model described in the talk.
- The talk's specific MCP servers (BigQuery, Looker, Google Cloud developer knowledge API) are Google-side integrations; their current availability and configuration should be verified against Google Cloud's own documentation, not Anthropic's.

---

## subagents

**Current status:** Subagents are specialized Claude Code workers that run in isolated context windows with custom system prompts, specific tool access, and independent permissions, used to offload tasks that would otherwise flood the main conversation context.

**Changes since talk:** The talk used "subagents" to describe Claude Code's parallelization capability for simulating team sprints. The current docs confirm this usage and have formalized it significantly. Key additions beyond what the talk described: custom subagent definitions (you define a reusable subagent by description so Claude auto-delegates to it), an "Agent view" for monitoring subagent work, "Run agent teams" as a distinct workflow, and "Isolate sessions with worktrees" as a companion pattern for parallel work. The context window visualization tool is new and specifically designed to show context savings from subagent delegation. The talk's framing of subagents as parallelizing task execution is accurate but understates the current isolation and reusability model.

**Key details for chapter:**
- Each subagent runs in its own context window with a custom system prompt and specific tool access. The primary use case is isolating side tasks (search results, logs, file contents) that would otherwise pollute the main conversation context.
- Custom subagents are defined as reusable configurations: when Claude encounters a task matching a subagent's description, it auto-delegates. This is distinct from ad-hoc parallelization.
- The "Run agent teams" workflow and "Agent view" are current features for orchestrating multiple subagents, which maps to the talk's "team sprint" analogy more directly than the talk's description implied was possible at the time.

---

## Improvement opportunities

- **Diagram: Subagent orchestration topology.** Flow chart showing the main Claude Code context spawning named subagents (PM subagent, UI subagent, security review subagent) with isolated context windows, each returning a result summary to the orchestrator. Should illustrate the context savings the docs reference and map directly to the talk's "team sprint" claim.

- **Code example: MCP server configuration for BigQuery.** A `.mcp.json` or equivalent config snippet showing how to wire a BigQuery MCP server to Claude Code, including the tool definition entries and any auth configuration (ADC passthrough). This is the most concrete missing artifact from the talk's analytics demo.

- **Comparison table: Google Cloud Claude hosting vs. Claude.ai.** Side-by-side showing pay-per-token vs. subscription, message caps (none vs. rate-limited), provisioned throughput availability, multi-region options, and ADC authentication support. The talk makes several distinct claims about Google Cloud advantages that are scattered in the transcript and would benefit from a single reference table.

- **Code example: Claude Code custom subagent definition file.** A CLAUDE.md or subagent config snippet defining a reusable "security review" subagent with a custom system prompt scoped to GCP IAM and Cloud Run security concerns, specific tool access (read-only file tools, no shell), matching what the talk demonstrated in its security review phase.

- **Diagram: End-to-end deployment pipeline.** Architecture diagram showing the full path from Claude Code prompts through Cloud Build CI/CD to Cloud Run, with Cloud Deploy handling production promotion. Should include where the security review subagent hooks in and where the developer knowledge API is consulted. Maps directly to the talk's CI/CD section.

- **Worked example: Bootstrapping a Cloud Run service with zero prior GCP knowledge.** Step-by-step showing a user prompting Claude Code to deploy a feedback API, with the developer knowledge API providing current Cloud Run documentation, the official Google Cloud skill executing `gcloud` commands, and the resulting Cloud Build trigger configuration. Illustrates the "no prior platform knowledge required" claim concretely.

- **Code example: CLAUDE.md configuration for a Google Cloud project.** A sample `CLAUDE.md` file that loads the Google Cloud developer knowledge MCP server, declares BigQuery and Looker MCP servers, and sets project-level context (GCP project ID, region). Shows readers exactly how to replicate the talk's setup in their own repo.
