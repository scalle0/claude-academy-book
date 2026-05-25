# Summary: From one person to 80: Scaling a hypergrowth engineering org with Claude Code

Chapter slug: `from-one-person-to-80-scaling-a-hypergrowth-engineering-org`

## Abstract

This talk presents Base44's engineering scaling journey from a single founder-engineer to 80 engineers, demonstrating practical applications of Claude Code throughout different growth phases. Base44, a visual coding platform acquired by Wix, faced distinct challenges at two scaling phases: 1-15 engineers and 50-80 engineers. For the first phase, they addressed onboarding, code review, and quality assurance using simple Claude prompts for organizational mapping, automated PR reviews based on historical feedback patterns, and frustration-level classification of user conversations for production monitoring. For the second phase at 50-80 engineers, they implemented automated experimentation workflows using historical AB testing data to generate guidelines, built evaluation systems using user simulators and automated testing with Stage Hand, and created QA automation through Claude Code skills that combine browser automation with database setup tools. The approach emphasizes simplicity over complex processes, leveraging past actions to encode organizational taste, dogfooding their own platform for internal tooling, and accepting that bottlenecks continuously shift as organizations scale.

## Key claims

- Simple Claude prompts analyzing commit history can replace traditional onboarding documentation and provide real-time organizational mapping
- Historical PR review patterns can be analyzed by Claude to create automated code review systems that replicate senior engineer feedback
- User frustration levels in chat conversations provide a stronger signal for product quality than traditional evaluation suites
- Past AB testing decisions can be analyzed to automatically generate experimentation guidelines and workflows
- User simulators combined with automated testing tools can create effective evaluation pipelines that test actual application correctness rather than just model outputs
- Claude Code skills can automate complex QA scenarios including database setup and edge case testing
- Dogfooding internal products accelerates feedback loops and improves development velocity
