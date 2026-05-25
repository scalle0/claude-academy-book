# Summary: The thinking lever

Chapter slug: `the-thinking-lever`

## Abstract

This talk examines test time compute techniques for improving Claude's performance through strategic token allocation during inference. The speaker presents evidence that increasing compute at test time produces intelligence gains comparable to scaling model parameters, demonstrated across multiple benchmarks including agentic coding tasks, reasoning problems, and computer use evaluations. Three primary mechanisms for test time compute are outlined: thinking (scratch pad reasoning), tool calling (external world interaction), and text output. The presentation introduces adaptive thinking, an evolution from interleaved thinking that allows Claude to autonomously determine when and how much to think rather than following predetermined patterns. User control mechanisms include effort levels (low to max) and budget constraints for token/time limits. Performance analysis reveals diminishing marginal returns at higher effort levels, with extra high effort representing an optimal balance between intelligence, speed, and token usage. The talk emphasizes that thinking should be treated as a core capability rather than an optional toggle, similar to how tool use is integrated into model workflows.

## Key claims

- Test time compute produces intelligence gains comparable to scaling model parameters at training time
- Performance increases logarithmically with token expenditure across knowledge domains including reasoning, computer use, and PhD-level examinations
- Adaptive thinking outperforms interleaved thinking by allowing Claude to autonomously choose when to engage reasoning versus tool calling or text output
- Larger models with low effort typically outperform smaller models with high effort on intelligence-requiring tasks
- Thinking should be enabled as a default capability rather than treated as an optional toggle for effort control
- Extra high effort level provides optimal Pareto efficiency between intelligence, latency, and token consumption
- Low effort levels can produce novel problem-solving approaches through constraint-induced creativity
