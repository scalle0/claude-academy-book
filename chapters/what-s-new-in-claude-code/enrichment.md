# Enrichment notes: What's new in Claude Code

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 2
Pages fetched: 2/2

---

## Claude Code

**Current status:** Claude Code is a full-featured AI coding assistant available across terminal CLI, VS Code, desktop app, web, and JetBrains IDEs, with installation via native installer, Homebrew, or WinGet.

**Changes since talk:** The fetched overview page rendered mostly as navigation scaffolding with minimal prose content, so a complete feature comparison is not possible from this fetch alone. Based on what is visible, the docs now organize features under explicit sections including "Agents and parallel work," "Automation," and "Platforms and integrations," which suggests the sidebar taxonomy has matured beyond what was described in the talk. The talk described many features as new; some of those (remote control, desktop app, code review) now have dedicated doc pages listed in the sidebar, indicating they have graduated from preview/new to stable documented features. No specific deprecations or renamed features are visible from the fetched content.

**Key details for chapter:**
- Installation is now available via a native installer script (`curl -fsSL https://claude.ai/install.sh | bash`), Homebrew, and WinGet, in addition to npm; the native installer is listed as recommended.
- The platform section in current docs lists "Remote Control," "Claude Code on the web," "Claude Code on desktop," "Chrome extension (beta)," "Computer use (preview)," "VS Code," "JetBrains IDEs," "Code review and CI/CD," and "Claude Code in Slack" as distinct integration surfaces, all of which were either absent or nascent at talk time.
- The "Automation" section in current docs lists "Automate with hooks," "Push external events to Claude," and "Run prompts on a schedule," which corresponds to what the talk called "routines" -- the production doc terminology may differ from the talk's terminology.

---

## git worktrees

**Current status:** The current docs describe worktrees under the "Agents and parallel work" section, with a dedicated page titled "Isolate sessions with worktrees" at `docs.anthropic.com/en/docs/claude-code/worktrees` (linked from the sidebar visible in the sub-agents page fetch).

**Changes since talk:** The fetched page for the `sub-agents` URL returned the "Create custom subagents" page, not a worktrees page. The sidebar on that page lists "Isolate sessions with worktrees" as a separate page. The talk used the term "work trees" as a parallel-session primitive; the current docs use the term "worktrees" (one word, matching the git CLI term `git worktree`). The talk presented worktrees primarily as a mechanism for running parallel Claude sessions without file conflicts; current docs frame them under the "Agents and parallel work" section alongside subagents and agent teams, suggesting the concept is now positioned as part of a broader orchestration model rather than a standalone dev-workflow feature. The specific worktrees page could not be fetched directly, so the full current details are not available from this fetch.

**Key details for chapter:**
- The canonical term in current docs is "worktrees" (one word), matching `git worktree` CLI terminology. The chapter should use this spelling consistently.
- Worktrees are now documented as part of the "Agents and parallel work" cluster alongside subagents, agent view, and agent teams, not as a standalone developer-experience feature.
- The `sub-agents` page (which the entity URL pointed to) is now titled "Create custom subagents" and covers a distinct concept: spawning specialized agents with custom system prompts, specific tool access, and independent permissions -- this is separate from worktrees, so the entity URL mapping in the original enrichment spec appears to conflate two different features.

---

## Improvement opportunities

- **Worktrees vs. subagents comparison table:** The talk conflates parallel sessions via worktrees with multi-agent orchestration. A side-by-side table showing worktrees (filesystem isolation, same repo, git-native) versus subagents (context isolation, custom system prompt, tool-scoped) versus agent teams (coordinated multi-agent runs) would clarify when to use each mechanism.

- **Auto mode decision flowchart:** The talk describes auto mode as assessing whether an action is "destructive or potentially malicious" before prompting for permission. A flowchart showing the decision path (action requested -> destructive check -> malicious check -> auto-approve or prompt) would make the permission model concrete. Include how this interacts with the existing permission modes documented at `docs.anthropic.com/en/docs/claude-code/permission-modes`.

- **CLAUDE.md vs. memory.md comparison table:** The speaker's analogy ("onboarding document" vs. "notes Claude takes while working") is clear in prose but a two-column table comparing scope, authorship, update frequency, and persistence would be more useful as a reference. Include example entries for each file.

- **Routines configuration example:** The talk describes routines as "a workflow that can be triggered based on an API call from another system," which maps to what current docs call "Run prompts on a schedule" and "Push external events to Claude." A concrete YAML or JSON config example showing a webhook-triggered routine (endpoint, schedule expression, prompt, and permission scope) would ground the concept. The chapter should also reconcile the talk's term "routines" with whatever term the production docs use.

- **Code review multi-agent architecture diagram:** The talk describes code review as spinning up "a team of different agents to assess different parts of that PR." A diagram showing the orchestration: PR created -> review orchestrator -> parallel specialist agents (security, logic, style, etc.) -> aggregated report would illustrate the multi-phase analysis claim.

- **Remote control session lifecycle diagram:** The talk describes starting a session on one device and accessing it from another. A sequence diagram showing device A (initiates session) -> Claude Code backend (session named, persisted) -> device B (mobile/browser, joins session) -> async work continues would clarify the remote control model and distinguish it from simple SSH tunneling.

- **Subagent definition file example:** The "Create custom subagents" page describes subagents with custom system prompts and tool access. A concrete example of a subagent definition file (fields: name, description, system prompt, allowed tools, permission scope) would show readers how to operationalize the pattern the talk describes for code review agents.

- **Installation method comparison table:** The overview page now lists four installation paths (native installer, Homebrew, WinGet, npm). A table comparing these by platform support, update mechanism, and enterprise governance compatibility would be useful given the talk's mention of native binaries for governance pipelines.
