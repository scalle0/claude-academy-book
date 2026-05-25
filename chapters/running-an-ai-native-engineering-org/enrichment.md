# Enrichment notes: Running an AI-native engineering org

Talk date: 
Enriched: today (live docs.claude.com fetch + Claude API)
Entities enriched: 3
Pages fetched: 3/3

---

## Claude

**Current status:** The current flagship model is Claude Opus 4.7, described as the most capable generally available model with a step-change improvement in agentic coding over Claude Opus 4.6.

**Changes since talk:** The talk predates the Claude 4 generation entirely. The current lineup (Opus 4.7, Sonnet 4.6, Haiku 4.5) represents a significant generational shift from whatever models were current at recording time. Notable structural changes: model IDs starting with the 4.6 generation use a dateless format (e.g., `claude-sonnet-4-6`) that is a pinned snapshot, not an evergreen pointer. Context windows are now 1M tokens for Opus and Sonnet. Opus 4.7 is explicitly positioned for agentic coding, which is directly relevant to the workflows described in the talk. Extended thinking is available on Sonnet 4.6 and Haiku 4.5 but not Opus 4.7; adaptive thinking is available on Opus 4.7 and Sonnet 4.6.

**Key details for chapter:**
- Claude Opus 4.7 (`claude-opus-4-7`) is the current recommended model for complex agentic coding tasks, at $5/MTok input and $25/MTok output.
- The 1M token context window on Opus 4.7 and Sonnet 4.6 is directly relevant to the talk's claim that code becomes the source of truth: entire codebases can fit in context.
- Models are available via Claude API, AWS Bedrock, Vertex AI, and Microsoft Foundry; the Claude Platform on AWS uses Claude API-style IDs, not Bedrock-style IDs.

---

## Claude Code

**Current status:** Claude Code is a production AI coding assistant available as a terminal CLI, VS Code extension, desktop app, web interface, and JetBrains plugin, installable via `curl -fsSL https://claude.ai/install.sh | bash`.

**Changes since talk:** The product has expanded significantly in surface area. At the time of the talk, Claude Code was primarily a CLI tool. Current docs show a substantially broader platform: desktop app, web interface (`Claude Code on the web`), Chrome extension (beta), computer use (preview), Slack integration, CI/CD integration, and a Remote Control feature. An Agent SDK is now documented. The `code.claude.com/docs/llms.txt` index endpoint exists for programmatic documentation discovery. Permission modes, session management, and a `.claude` directory for storing instructions and memories are all documented features.

**Key details for chapter:**
- Claude Code now supports multiple surfaces beyond the terminal: VS Code, JetBrains, desktop app, web, and Slack, which expands the "dogfooding" scenario the speaker describes beyond CLI-only workflows.
- The `.claude` directory provides persistent memory and instruction storage across sessions, directly supporting the talk's point about code and context replacing documentation.
- Third-party model providers are supported in the Terminal CLI and VS Code surfaces, meaning Claude Code is not exclusively tied to Anthropic-hosted Claude models.

---

## MCP

**Current status:** The MCP documentation page at `https://docs.anthropic.com/en/docs/agents-and-tools/model-context-protocol` returned a 404 Not Found response.

**Changes since talk:** The page failed to fetch. Based on training data: MCP (Model Context Protocol) is an open protocol Anthropic published for connecting AI models to external tools and data sources via a standardized server/client architecture. The Claude Code docs sidebar confirms MCP remains a supported extension mechanism for Claude Code specifically. The canonical MCP documentation has likely moved; the spec and SDK documentation now live at `modelcontextprotocol.io` rather than Anthropic's own docs domain. The Claude Code overview page references "Extend Claude Code" as a section, which covers MCP server integration. The chapter should not rely on the URL provided for this entity.

**Key details for chapter:**
- MCP documentation has moved off `docs.anthropic.com`; the authoritative source appears to be `modelcontextprotocol.io` (caveat: based on training data, not a live fetch).
- Claude Code's "Extend Claude Code" section in current docs covers MCP server integration as the primary extensibility mechanism.
- MCP enables the cross-functional blur the speaker describes: a single engineer can wire Claude Code to internal tools (databases, CI systems, issue trackers) without building custom integrations, which is the practical mechanism behind several of the org structure claims.

---

## Improvement opportunities

- **Comparison table: Traditional vs. AI-native engineering process.** Side-by-side table covering planning (design doc vs. prototype), code review focus (style/bugs vs. risk/product sense), bottleneck (engineering bandwidth vs. verification), source of truth (docs vs. code), and team structure (specialist silos vs. generalist with deep roots). Maps directly to the talk's central argument.

- **Diagram: AI-native PR workflow.** Flow chart showing the changed review loop: AI-assisted commit, automated verification, reviewer focus on risk tier classification and product sense, with a decision branch for "acceptable risk" vs. "needs human judgment." Illustrates the talk's claim that review must shift from syntax to semantics at higher throughput.

- **Code example: Claude Code CLAUDE.md configuration for a new engineer.** A sample `.claude/CLAUDE.md` file demonstrating how team norms, architecture conventions, and codebase-specific context get encoded as persistent instructions, replacing the onboarding wiki the talk implicitly deprecates.

- **Code example: MCP server wiring Claude Code to an internal tool.** A minimal MCP server config (JSON or TypeScript) exposing one internal tool (e.g., a CI status checker or internal search index), illustrating the mechanism by which individual engineers can extend Claude Code's context without platform-team involvement. Flag that the canonical MCP docs URL provided has moved.

- **Comparison table: Claude model selection for agentic coding tasks.** Three-column table (Opus 4.7, Sonnet 4.6, Haiku 4.5) covering cost per MTok, context window, adaptive/extended thinking availability, latency tier, and recommended use case within an engineering workflow (Opus for long autonomous tasks, Sonnet for interactive sessions, Haiku for high-frequency small tasks like test generation).

- **Worked example: Prototype-driven design decision.** End-to-end scenario where a team skips a design doc and instead uses Claude Code to produce two competing implementations of a proposed API change, then resolves the debate via PR comparison. Concretizes the "code wins" quote and shows the workflow mechanics.

- **Diagram: Verification bottleneck under increased throughput.** Before/after throughput diagram showing that as AI raises commit rate, the verification layer (tests, linting, security scanning, staging deployment) becomes the new rate limiter. Motivates the talk's claim that QA investment must scale proportionally with AI adoption.

- **Comparison table: Code ownership model before and after.** Two-column table contrasting traditional `CODEOWNERS`-style accountability (named humans, blame-based review) with the AI-native framing the speaker introduces (intent-based ownership, root-cause review). Addresses the "who made this change" quote directly.
