# Summary: Getting more out of the Claude Platform

Chapter slug: `getting-more-out-of-the-claude-platform`

## Abstract

This talk presents optimization strategies for the Claude platform to improve production agent performance and reduce costs. The presentation covers four primary techniques: prompt caching for 90% token cost reduction and improved latency, context engineering through tool search and programmatic tool calling to maximize context efficiency, conversation compaction for extended context management, and advisor strategy pairing lower-cost models with high-intelligence oversight. The speaker demonstrates these techniques through a live demo of HeroCorp, a superhero staffing platform, showing cost reductions from over 30 pounds to 11 pounds while maintaining intelligence quality. Key platform features discussed include automatic prompt caching, analytics dashboards for cache hit rate monitoring, and the Claude API skill for implementation guidance. The talk emphasizes the importance of examining agent transcripts to understand model behavior and implementing systematic approaches to context management for production deployments.

## Key claims

- Prompt caching provides 90% cost savings, rate limit improvements, and latency reduction for cached tokens
- Context engineering through tool search can reduce overall token consumption by 10% while improving model performance
- Programmatic tool calling allows models to curate tool results by writing Python scripts to filter relevant content
- Conversation compaction enables near-unlimited context by summarizing and removing irrelevant conversation turns
- Advisor strategy pairs lower-cost models with high-intelligence oversight to achieve Pareto optimal cost-intelligence trade-offs
- Production agents should target 80% or higher prompt cache hit rates, with top customers achieving 90%+ rates
- Context engineering requires examining agent transcripts to understand what models actually process
