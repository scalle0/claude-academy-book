<!--
Source: "Beyond the Basics with Claude Code", Daisy Holman, Code with Claude London 2026
Corpus: chapters/beyond-the-basics-with-claude-code/
Target length: 5200 words
Editor queries: 2
Fidelity audit: see below
Enrichment deltas applied: 3
Cross-references inserted: 1
-->

# Customising Claude Code for Large-Scale Software Engineering

## 1. The customisation problem

Claude Code works well out of the box for zero-to-one projects: fresh repositories with no conventions, no accumulated technical debt, and no stakeholders whose concerns live outside the codebase. The moment a project crosses into professional software engineering, that default capability is no longer sufficient.

The gap has three dimensions: access, knowledge, and tooling.

**Access** is the most consequential. A software engineer's work does not live exclusively in source code. Decisions are made in Slack threads. Requirements are refined in design documents. Post-incident responses depend on dashboards and runbooks. CI/CD pipelines determine whether a change ships. Meeting transcripts contain action items that never make it into a ticket. If Claude cannot reach the same information sources a human developer routinely consults, it cannot participate as a colleague in that workflow.

The practical test: spend a full day working without leaving the Claude Code terminal. Every time you reach for another tool, every time you copy-paste from a browser into a prompt, write it down. That list is the set of connections Claude is missing. Closing those gaps produces disproportionate improvement because the information was always available somewhere; it was just inaccessible to the agent.

**Knowledge** encompasses codebase conventions, institutional memory, internal vocabulary, and internal APIs. None of this can be trained into the model weights (more on this in section 3). It must be provided through in-context learning: text files, skills, CLAUDE.md, and tools. Most teams underinvest here. They write a one-paragraph CLAUDE.md and assume the agent will figure out the rest.

**Tooling** is the third dimension. Claude's default editing interface is primitive. It writes the exact string it wants to replace and the exact string it wants to insert. No syntax highlighting, no code completion, no inline error markers. In the evolution of text editors, this is ED, not Vim. The question to ask is: what does the IDE for Claude look like? What does the agentic equivalent of code completion look like? What does the agentic equivalent of those red squiggly underlines look like, the ones that nudge you toward a correction without stopping you?

The thesis is simple: if Claude cannot do everything you can do, it cannot do your job with you. The role of the software engineer in an agentic workflow is to create capable clones of yourself, each with access to the information, knowledge, and tools they need.

## 2. The context window constraint

Every customisation that enters the model passes through the context window. There is no other path. The context window is a fixed-size container, and its capacity is not growing. Model capabilities have improved dramatically over the past year; context window sizes have not. A few models offer 200,000-token windows. A few offer a million. But the frontier of context window size is flat.

This makes context engineering a constrained optimisation problem. It is like trying to run NPM on an Arduino: a small amount of memory, a large number of things competing for space, and a hard requirement to leave enough room for the actual work. Installing packages indiscriminately on an Arduino leaves no room for application code. Filling a context window with tool definitions and background documents leaves no room for reasoning.

The zero-overhead abstraction principle applies directly. Originally a C++ design philosophy ("don't pay for what you don't use"), it is not a nice-to-have in context engineering. It is a hard constraint. The context window is not getting bigger. The only way to fit more useful information in is to stop paying for information that is not relevant to the current task.

### KV cache economics

The constraint is more nuanced than a simple size limit. The KV cache determines how expensive it is to compute the next token. Content at the beginning of the prompt is cached and reused across turns. Content later in the prompt may be uncached if anything before it changes.

The cost asymmetry is significant. If you change something early in the prompt, every token after that change becomes uncached, costing roughly ten times more to process. This invalidates the intuitive approach of treating the context window like an LRU cache, evicting recently unused tools and replacing them with currently needed ones. Swapping out a tool definition near the top of the system prompt invalidates the cache for everything that follows.

The current pricing model for prompt caching reinforces this structure. Cache writes cost 1.25x the base token price for the default five-minute TTL, or 2x for a one-hour TTL. Cache hits cost 0.1x. The economics reward stability at the front of the prompt and volatility at the end.

The practical rule: stable, shared content (tool definitions, system instructions, CLAUDE.md) goes at the very front of the context. Volatile, per-task content (file contents, conversation history, task-specific instructions) goes toward the end, where it can be replaced without invalidating the cache for everything before it.

## 3. Why not fine-tuning

Fine-tuning is the first suggestion most teams raise when they want Claude to learn their codebase conventions. It does not work well for this purpose, for two reasons.

First, research from late 2025 indicates that fine-tuning large language models on specialised information can increase hallucination rates. The model becomes more confident about the fine-tuned domain but less reliable in distinguishing what it actually knows from what it is pattern-matching.

Second, it is not cost-efficient at the frontier. Model releases are frequent enough that by the time a large organisation completes a fine-tuning cycle, the base model has moved on. The investment does not carry forward.

The alternative is in-context learning (ICL). The term sounds technical; the reality is text files. Skills, CLAUDE.md, tool descriptions, and conversation history are all forms of ICL. Everything Claude knows about your codebase, your conventions, and your preferences is provided through text in the context window.

This is consistent with the bitter lesson in AI research: general methods that leverage computation outperform specialised methods in the long run. Frontier models are general. Customisation through ICL keeps the customisation portable, versionable, and decoupled from model weights.

## 4. The four plugin primitives

Claude Code exposes four customisation primitives: MCP servers, skills, hooks, and sub-agents. Each serves a different purpose. The critical question for large-scale engineering is not "what can this primitive do?" but "what happens when I have 10,000 of them in a monorepo?"

### MCP

The Model Context Protocol was designed in an era when agents were simpler. Its original target was chatbots running serverless, with no shell access and no local filesystem. MCP provides a transport-agnostic way to inject tools into the context, handles authentication, and is the right choice for public integrations: if a company wants to ship an integration with Claude to external customers, it should probably be an MCP server.

For internal developer tooling in a monorepo, MCP is often unnecessary overhead. If the developer already has shell access and a CLI, wrapping that CLI in an MCP server adds process lifecycle management, authentication setup, and system prompt bloat without clear benefit. A skill that teaches Claude how to use the CLI directly is simpler to write and maintain.

MCP does not scale. Each tool requires its name, description, and schema to be placed in the system prompt so the model knows how to call it. Twenty servers with fifteen tools each can consume the majority of a context window with tool definitions alone.

Tool search partially mitigates this. Instead of loading every tool's full schema, only tool names go into the system prompt. Claude has a meta-tool to search for tools by name, loading the full description and schema on demand. This is lazy loading for tool definitions. It helps, but it is not free: the more you compress the description, the less likely Claude is to know it should search for a given tool. Generic tools (edit, bash) still need their full schemas in the system prompt.

### Skills

A skill is a folder containing a SKILL.md file with frontmatter that includes a one-line description. The description goes into the system prompt. The body loads only when Claude decides the skill is relevant. This is a lazy system prompt: pay for the body only when you use it.

Skills are easy to create, which is both an advantage and a risk. In a monorepo, the ease of creation means skills proliferate quickly, and quality control becomes a real concern.

Scalability is better than MCP but still limited. The one-line description is always loaded; you always pay that fraction of your context window. Reliably triggering a skill without explicit user mention can require a description of 300 to 400 tokens. There is no hierarchy mechanism to lazily expose sub-skills, though this is actively being developed.

### Hooks

Hooks are the closest thing to a true zero-overhead abstraction in the plugin system. A hook is a script that runs in response to an event in the agentic loop (pre-tool-use, post-tool-use, session start, session end, user prompt submit, stop). The script receives a JSON payload describing the event, decides whether it is relevant, and optionally returns text to inject into the context window.

The key property: if a hook does not match, it costs zero tokens. The script runs on the host machine, outside the context window entirely. If 100,000 hooks are registered and 99,995 of them do not match the current event, the only cost is local compute. The constraint has shifted from the scarce resource (context window) to an abundant one (CPU cycles on the developer's machine).

Current hook implementations support three types: command hooks (shell scripts), HTTP hooks (endpoints), and MCP tool hooks. They fire on six lifecycle events: SessionStart, SessionEnd, UserPromptSubmit, Stop, PreToolUse, and PostToolUse.

This is where the "red squigglies" pattern lives. A post-tool-use hook can run a linter after every edit, check whether a file is generated, or validate that a change conforms to codebase conventions. Like the red underlines in an IDE, it nudges the agent without hard-blocking it. The agent can override the nudge if it has a good reason, but the reminder is usually enough to prevent mistakes.

Hooks cannot do everything. Matching logic is typically regex or string parsing on the tool call payload, which limits expressiveness. Using a sub-agent to decide whether to inject content is possible but expensive from a token perspective.

### Sub-agents

A sub-agent is a specialised Claude instance with its own system prompt, tool access, and permissions. Its description sits in the parent agent's system prompt. When triggered, the sub-agent's work happens in a separate context window: the parent pays only for the tool call and the result, not for the sub-agent's internal reasoning.

Sub-agents scale well for offloading work. A sub-agent can read 50 files so the main loop does not have to. But the descriptions still accumulate in the parent prompt. With 100,000 sub-agents in a monorepo, you face the same system-prompt bloat as with skills.

### Why CLAUDE.md cannot be plugin-provided

A frequent request is to allow plugins to provide a CLAUDE.md fragment that loads unconditionally into the user's context when the plugin is enabled. This would not scale. Every plugin would provide one. Each would add "just a little bit of text." At scale, those fragments would consume the context window before the user types a prompt.

The explicit-cost alternative: return text from a session-start hook. This makes the cost visible and deliberate, rather than hidden inside a plugin's metadata.

## 5. Feedback loops over smarter models

The fastest way to make an agent better at a codebase is not a smarter model. It is a tighter feedback loop.

Most of the feedback scripts teams need already exist. Developer environment setup created linters, type checkers, test runners, and deployment validators. These tools were built for human developers. They work equally well as hook targets for agents.

The distinction that matters: tools that compensate for a lack of intelligence versus tools that scale with intelligence. A rule that hard-blocks the agent from using an undefined variable compensates for lack of intelligence. It prevents a specific class of error, but it constrains how the agent works and does not improve as the model improves. A post-tool-use hook that flags the undefined variable (the red squiggly) scales with intelligence. A less capable model benefits from the reminder. A more capable model overrides it when appropriate.

The design principle: build overridable nudges, not hard blocks. The agentic equivalent of syntax highlighting, code completion, and error markers. The tools human developers use to write better code, adapted for an agent that works differently but benefits from the same feedback signals.

## 6. Workflows for parallelism and async work

Two properties define the next phase of agentic software engineering: asynchrony (walk away, let it work, come back) and parallelism (multiple agents working concurrently). Both require getting comfortable with context switching, even for engineers who prefer deep flow states.

### Git worktrees

The baseline for parallel agent work. A git worktree is a separate checkout of the same repository in a different directory. Each worktree gets its own Claude Code instance. Agents in different worktrees cannot step on each other, the same way human colleagues working in separate checkouts cannot create merge conflicts until they push.

Long-lived worktrees avoid the overhead of re-running environment setup (dependency installation, symlink creation) for each new task. Each worktree tracks upstream main. Each hosts a persistent agent with its own identity and session history.

### Session identity

Renaming sessions and assigning colours reduces context-switching latency. Colour triggers spatial memory efficiently. This is "syntax highlighting for humans in the agentic era": a small investment in visual differentiation that pays back every time you switch between sessions.

### Agent teams and cross-agent communication

Agents running on the same account can send messages to each other using the send-message tool. This matters because one of the information sources an agent needs access to is another agent's conversation. If agent A is working on a feature and agent B needs context about that feature, the message tool provides it without requiring the human to copy-paste between sessions.

### Slash loop

Slash loop runs a prompt at a fixed interval. The primary use case: unattended CI monitoring. After pushing a PR, `/loop 10m check CI status and fix failures` lets the agent babysit the pipeline through multiple CI cycles, even overnight. The agent can turn off the loop when the prompt is no longer relevant. This is what makes pipelining practical: work on the next task while the previous one grinds through CI.

### Auto mode and permissions

Auto mode removes interactive permission prompts, replacing them with a classifier agent and an adversarial safety check. This is the enabler for async and overnight work. Slash loop is not usable if the agent stops every few minutes to ask for file-write permission. The tradeoff is higher token cost (the safety classifier consumes additional tokens per tool call).

For details on these features, see Chapter: What's New in Claude Code.

## 7. Three principles

**Give it access.** Every tool you reach for outside the Claude Code terminal is a connection Claude is missing. Close those gaps.

**Mind the box.** The context window is fixed. Every customisation competes for space. Stable content at the front, volatile content at the end, and nothing that does not earn its place.

**Pick abstractions that scale.** Ask what happens with 100,000 instances. If the answer is "the system prompt overflows," choose a different primitive.

## Editor queries

1. **[EDITOR QUERY: lines 140-141]** The transcript is garbled around the discussion of context window size trends ("severally Ramadan world performed... N¨"). The surrounding context indicates the speaker was noting that context windows haven't grown much recently while models have improved. The chapter paraphrases this from context, but the specific data points (if any were mentioned) are lost.

2. **[EDITOR QUERY: lines 203-208]** A heavily garbled passage ("nonprofit угарda server space", "obesity issue", "Nelson, weBI") appears to discuss MCP's assumptions about server environments and how customisations are shared across agents. The chapter omits this passage; if the original point was important, it would need to be recovered from the video.

## Fidelity audit

| Claim in chapter | Transcript support | Verdict |
|---|---|---|
| If Claude can't do everything you can do, it can't do your job with you | Line 21: "if Claude can't do everything you can do, it can't do your job with you" | Supported (verbatim) |
| Three categories: access, knowledge, tooling | Lines 19-20: "Access, knowledge, and tooling" | Supported |
| Team chat, CI/CD, dashboards, internal docs as access needs | Lines 45-61 | Supported |
| Spend a full day without leaving the terminal, note every alt-tab | Lines 63-66 | Supported (paraphrased) |
| Fine-tuning leads to more hallucinations (late-2025 papers) | Lines 72-73: "papers from late 2025... fine tuning on specialized information can lead to more hallucinations" | Supported |
| Fine-tuning not cost-efficient for frontier models | Lines 74-75: "frontier models are churning so quickly... fine tuning on a model, the frontier model just isn't cost efficient" | Supported |
| ICL is "just text files" | Line 79: "you're actually just talking about text files" | Supported (paraphrased) |
| The bitter lesson applies | Lines 79-80: "because of the bitter lesson... general AI wins out over specialized AI" | Supported |
| Context window sizes are staying constant | Lines 141-143: "the frontier of context windows hasn't changed... remaining relatively constant" | Supported |
| NPM on an Arduino analogy | Lines 149-151 | Supported (verbatim metaphor) |
| Zero-overhead abstraction principle from C++ | Lines 155-157 | Supported |
| KV cache: changing early tokens makes rest uncached at 10x cost | Lines 168-169: "uncached tokens, which cost ten times as much for all of the rest of your context window" | Supported |
| MCP designed for chatbots/serverless | Lines 192-195 | Supported |
| MCP doesn't scale: 20 servers x 15 tools fills context | Lines 215-217 | Supported |
| Tool search as partial mitigation | Lines 219-225 | Supported |
| Skills: lazy system prompt, body pay-per-use | Lines 235-237 | Supported |
| Skills: 300-400 tokens to reliably trigger | Line 243 | Supported |
| No skill hierarchy yet | Lines 244-246 | Supported |
| Hooks: zero-overhead, run outside context | Lines 250-257 | Supported |
| Red squigglies pattern for hooks | Lines 101-109, 263 | Supported |
| Sub-agents: description in parent, work in separate context | Lines 265-271 | Supported |
| CLAUDE.md cannot be plugin-provided (wouldn't scale) | Lines 279-286 | Supported |
| Session-start hook as alternative | Lines 288-289 | Supported |
| Fastest improvement: tighter feedback, not smarter model | Lines 122-123: "The fastest way to make your agent better... isn't a smarter model. It's a tighter feedback loop" | Supported (verbatim) |
| Tools that scale with intelligence vs compensate for lack of it | Lines 131-137 | Supported |
| Git worktrees for parallel work | Lines 309-312 | Supported |
| Session colour as context-switching aid | Lines 315-317 | Supported |
| Send-message tool for agent communication | Lines 332-337 | Supported |
| Slash loop for CI babysitting | Lines 339-345 | Supported |
| Auto mode / permissions mode | Lines 348-358 | Supported |
| Three take-homes: give it access, mind the box, pick abstractions that scale | Lines 373-377 | Supported |
| Prompt caching pricing (1.25x write, 0.1x hit) | Enrichment (docs.anthropic.com) | Enrichment delta |
| Hooks: three types, six lifecycle events | Enrichment (docs.anthropic.com) | Enrichment delta |
| Skills: custom commands merged into skills system | Enrichment (docs.anthropic.com) | Enrichment delta |
