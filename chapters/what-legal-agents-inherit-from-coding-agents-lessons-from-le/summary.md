# Summary: What legal agents inherit from coding agents: Lessons from Legora

Chapter slug: `what-legal-agents-inherit-from-coding-agents-lessons-from-le`

## Abstract

This talk examines how legal AI agents can leverage design patterns and technical approaches developed for coding agents. Jacob Emmerling from Legora presents a framework for building domain-specific AI agents by categorizing learnings from coding agents into three buckets: direct reuse (planning, human-in-the-loop, sandboxes), translation (adapting patterns like document editing loops and linting), and domain-specific invention (citations, due diligence workflows). The presentation demonstrates how Legora rebuilt their legal document editing system by translating the read-edit-verify loop pattern from coding agents, replacing their previous multi-model handoff architecture with a single-agent approach using intermediate document representations. Key examples include implementing planning modes for legal tasks, approval workflows for dangerous actions, and ESLint-style linting for legal documents. The talk concludes with live demonstrations of collaborative legal document editing and mass document review using tabular extraction tools, showing how domain-specific features like citation tracking and redlining integrate with patterns borrowed from coding agents.

## Key claims

- Legal work and coding share fundamental similarities including text-based documents, strict conventions, and review cultures
- Coding agents are significantly ahead of other vertical domains in AI adoption and capability
- Agent development patterns can be categorized into reusable, translatable, and domain-specific invention buckets
- Single-agent document editing loops outperform multi-model handoff architectures for legal document editing
- Intermediate document representations enable coding-style editing patterns for complex formats like DOCX
- Static analysis and linting patterns from coding can be applied to legal document validation
- Tool design similarity to coding agents provides benefits from existing reinforcement learning and fine-tuning
