# Fidelity audit: Beyond the Basics with Claude Code

Chapter: `beyond-the-basics-with-claude-code`

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
