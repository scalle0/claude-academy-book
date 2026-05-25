# Summary: Picking the right model

Chapter slug: `picking-the-right-model`

## Abstract

This talk presents a systematic approach to model selection for production AI applications. The speaker argues that public benchmarks provide insufficient guidance for specific use cases and advocates for building custom evaluations based on three pillars: model quality, latency, and cost. The presentation emphasizes that the optimal model is not necessarily the cheapest per token, but rather the cheapest per successful outcome. The talk covers common evaluation pitfalls including noise versus signal confusion, infrastructure failures, and silent saturation. It introduces strategies for optimizing the cost-accuracy frontier through thinking modes, effort levels, prompt caching, and context engineering. The workshop demonstrates running evaluations across multiple models and configurations using TauBench, revealing counterintuitive findings where higher-intelligence models sometimes achieve better performance with lower latency and token consumption than smaller models.

## Key claims

- A small, well-designed custom evaluation provides more actionable insights than public benchmarks for specific use cases
- The optimal model choice should optimize for cost per successful outcome rather than cost per token
- Higher-intelligence models can sometimes achieve better performance with lower latency and fewer tokens than smaller models
- Prompt caching can reduce input token costs by 90% when implemented correctly with cache hit rates of 80-90%
- Context engineering and hygiene can reduce token consumption by 65-77% while improving accuracy
- Public benchmarks are directional but fail to represent heterogeneous production workloads
- Model behavior varies significantly between versions, requiring prompt adjustments for each model variant
