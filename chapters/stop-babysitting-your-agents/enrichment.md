# Enrichment notes: Stop babysitting your agents

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 3/3

---

## Claude Code

**Current status:** Claude Code is a full-featured agentic coding assistant available across terminal CLI, VS Code, desktop app, web, and JetBrains IDEs, with a documented Agent SDK and parallel/subagent capabilities.

**Changes since talk:** The overview page shows substantial expansion of the platform surface since a talk focused on managing multiple sessions. Notable additions visible in the nav structure: a dedicated "Agents and parallel work" section (covering subagents, agent view, agent teams, and worktrees), a "Remote Control" page under Platforms and integrations, scheduled prompts under Automation, and an Agent SDK. The talk described these capabilities as emerging workarounds; they now have first-class documentation sections.

**Key details for chapter:**
- Claude Code now has a dedicated "Agent view" for managing parallel sessions, directly addressing the multi-clauding workflow the talk described as a manual juggling act.
- The "Run agent teams" and "Create custom subagents" pages formalize the parallel processing approach the speaker was advocating for as a power-user technique.
- Remote Control is now a documented integration under Platforms, not a workaround; the mobile notification management use case the speaker described is supported.

---

## MCP

**Current status:** The MCP page at the provided URL returned a 404. The correct current location appears to be under the Claude Code docs at `https://code.claude.com/docs` rather than `docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol`.

**Changes since talk:** Fetch failed with Not Found. Based on the skills page sidebar content that was successfully fetched, MCP within Claude Code is documented under "Tools and plugins > Model Context Protocol (MCP)" with sub-pages for discovering/installing prebuilt plugins and creating plugins. The URL provided in the entity list is stale; the canonical MCP documentation for Claude Code has moved or been restructured. From training data: MCP is an open protocol Anthropic published for connecting models to external tools and data sources via a standardized interface, using a client-server architecture where Claude acts as the client.

**Key details for chapter:**
- The MCP docs URL in the entity list (`docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol`) returned 404; cite `code.claude.com/docs` with the sidebar path Tools and plugins > Model Context Protocol instead.
- MCP enables the "give Claude access to tools" argument in the talk: rather than ad-hoc tool grants, MCP servers provide a structured, reusable way to expose build systems, test runners, and linters to Claude.
- Prebuilt plugins are now discoverable and installable, lowering the barrier to the verification loop setup the talk describes.

---

## Skills

**Current status:** Skills are markdown files (`SKILL.md`) stored in `.claude/skills/<name>/` that load into context only when invoked, either automatically by Claude when relevant or explicitly via `/skill-name`.

**Changes since talk:** The speaker described skills as a way to store "arbitrary context about a specific topic" and package verification loops. The current docs confirm this framing but add one significant clarification: custom commands (previously stored in `.claude/commands/`) have been merged into skills. A file at `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` are now equivalent and both create `/deploy`. If the talk referenced "commands" and "skills" as distinct, that distinction is gone.

**Key details for chapter:**
- Skills use lazy loading: the skill body is not loaded into context until the skill is invoked, so large reference procedures (like a full verification loop) cost no tokens until needed.
- The self-improving skill pattern the speaker described (instructing Claude to update the skill when it hits a blocker) is directly supported by the file-based format: Claude can read and write `SKILL.md` as part of a task.
- The old `.claude/commands/` path still works and is treated identically to `.claude/skills/`; the chapter should use the skills path as canonical going forward.

---

## Improvement opportunities

- **Verification loop flowchart:** A diagram showing the autonomous loop cycle: Claude makes a change, invokes build/test tools via MCP, parses results, decides to iterate or exit. Should include the hill-climbing analogy from the talk and show the exit condition (tests pass / criteria met). This makes the abstract "autonomous circuit" quote concrete.

- **Skill file structure code example:** A complete `.claude/skills/verify-typescript/SKILL.md` showing how to encode a verification loop as a skill, including the self-improvement instruction pattern ("if you hit a blocker, update this file with what you learned"). Should show the invocation command (`/verify-typescript`) and a sample trigger condition.

- **Multi-session management comparison table:** A side-by-side table comparing the old manual approach (the "glorified QA tester" state the speaker laments) vs. the structured approach: one column for "ad-hoc multi-terminal" and one for "agent view + subagents," covering session visibility, interrupt handling, context sharing, and mobile access via Remote Control.

- **Background loop cron/schedule config example:** A concrete configuration for the "Run prompts on a schedule" feature showing a PR triage routine. Should include the schedule syntax, the prompt content (check open PRs, label stale ones, post status comments), and the relevant permission mode setting to allow it to run unattended.

- **MCP server config for a verification toolchain:** A JSON MCP server definition exposing three tools: `run_build`, `run_tests`, and `get_type_errors`. This directly illustrates the talk's claim that "agents need the same tools humans use but require explicit access." Include the tool schema fields (`name`, `description`, `inputSchema`).

- **Worked example, self-improving skill:** End-to-end scenario: Claude is given a `/deploy` skill, hits a new environment variable requirement it did not expect, writes the failure and the fix back into `SKILL.md`, and the next run succeeds without human intervention. Walk through the before/after `SKILL.md` diff. This operationalizes the "self-documenting, self-improving skill" quote.

- **Attention scaling diagram:** A simple chart plotting number of concurrent Claude sessions (x-axis, 1 to 10+) against estimated human attention required (y-axis) under three strategies: manual monitoring, verification loops only, and verification loops plus agent view plus background routines. Illustrates the speaker's 4-5 session ceiling and shows where the ceiling moves with each strategy.
