# Summary: The prompting playbook

Chapter slug: `the-prompting-playbook`

## Abstract

This presentation covers systematic approaches to prompt engineering and optimization for large language models in production environments. The talk addresses two primary scenarios: maintaining and debugging existing prompts when migrating to new models, and building new agentic systems from scratch. Using a customer support bot example for a telecommunications company, the speaker demonstrates how to establish evaluation suites with control cases, edge cases, and capability boundary tests. The methodology involves applying general hygiene principles such as XML structuring, removing redundant instructions, and creating clear output contracts. Key optimization techniques include avoiding patches from previous models that may cause overfitting, providing tools rather than relying on instructions alone for complex tasks, and balancing trade-offs in escalation scenarios. For new agent development, the presentation compares monolithic prompts against multi-step agentic approaches using a staff scheduling example. The analysis examines different models including Claude Sonnet and Opus variants, with and without adaptive thinking, demonstrating how decomposing complex tasks into generate-evaluate-repair loops can achieve better performance with lower token usage. The talk emphasizes the importance of rigorous evaluation frameworks and systematic debugging approaches rather than ad-hoc prompt modifications.

## Key claims

- Evaluation suites are essential for rigorously testing prompt performance and must include control cases, edge cases, and capability boundary tests
- General hygiene principles like XML structuring and removing redundant information can immediately improve prompt performance
- Instructions alone do not add capability; tools and structured approaches are required for complex tasks like calculations
- Models can withhold information they have access to due to overly defensive instructions from previous model patches
- Agentic approaches using generate-evaluate-repair loops can outperform monolithic prompts in both token efficiency and task completion
- Different models require different prompting strategies, and larger models with reasoning capabilities may need fewer prompt optimizations
- Multi-step prompt systems allow for runtime flexibility in handling soft constraints without modifying evaluation functions
