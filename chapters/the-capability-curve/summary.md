# Summary: The capability curve

Chapter slug: `the-capability-curve`

## Abstract

This talk examines the rapid advancement in AI coding capabilities over the past 12 months, focusing on Claude's evolution from basic code assistance to autonomous software engineering. The speaker presents evidence of dramatic improvements in coding benchmarks, with Claude advancing from 60% to 87% on SweeBench verified, and demonstrates the capability differences through a live comparison of rebuilding the Claude.ai website. Three key areas drive these intelligence gains: improved planning and reasoning before acting, better error recovery and adaptation to failure, and sustained attention over long agentic runs. These improvements enable autonomous agents capable of multi-hour execution, as exemplified by a complete rewrite of the Bun JavaScript engine from JavaScript to Rust in one week. The talk provides practical guidance for adapting to this capability curve, emphasizing the importance of building robust evaluations that measure real use cases, shrinking scaffolding and prompts as models become more capable, and giving models room to work through adaptive thinking, autonomous operation, and closed-loop agent improvement.

## Key claims

- Claude has advanced from solving 60% to 87% of SweeBench verified issues in 12 months, representing a 3x improvement in GitHub issue resolution
- Modern frontier models have saturated existing benchmarks like SweeBench verified, making it difficult to measure continued progress
- Models now demonstrate autonomous planning and reasoning before acting, eliminating the need for extensive scaffolding to force planning behavior
- Error recovery has dramatically improved, with models no longer falling into doom loops and instead adapting their approach after failures
- Long-horizon coherence allows models to maintain attention and task focus across millions of tokens without losing context
- Autonomous agents can now run for many hours rather than just minutes, enabling complete software projects like rewriting entire codebases
- The Bun JavaScript engine was completely rewritten from JavaScript to Rust in one week using Claude agents with nearly 100% test coverage
