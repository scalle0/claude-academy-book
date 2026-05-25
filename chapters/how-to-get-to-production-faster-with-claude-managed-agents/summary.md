# Summary: How to get to production faster with Claude Managed Agents

Chapter slug: `how-to-get-to-production-faster-with-claude-managed-agents`

## Abstract

This talk introduces Claude Managed Agents, Anthropic's platform for building production-ready AI agent systems. The speakers argue that while AI model capabilities have grown exponentially from Claude 3 to Claude 4.7, infrastructure rather than intelligence has become the primary bottleneck for agent deployment. Claude Managed Agents addresses key development challenges including context management, memory systems, reliability, scalability, and observability. The platform provides composable primitives including agent definitions (system prompts, models, skills, tools, permissions), sandboxed execution environments, event streaming for real-time monitoring, and advanced features like multi-agent orchestration, outcomes-based iteration, persistent memory, and dreaming capabilities. New features announced include self-hosted sandboxes for running agent compute within customer VPCs and MCP Tunnels for secure access to private Model Context Protocol servers. The platform aims to reduce infrastructure complexity so developers can focus on building agent applications rather than managing underlying systems.

## Key claims

- Infrastructure around AI models, not model intelligence, has become the primary bottleneck for scaling agent capabilities
- Claude Managed Agents provides managed infrastructure including context management, memory, reliability, scalability, and observability
- The platform supports multiple interaction paradigms including conversational, outcome-oriented, and asynchronous agent workflows
- Multi-agent orchestration allows Claude to spawn specialized agent threads with separate context windows for task delegation
- Self-hosted sandboxes enable customers to run agent compute within their own VPCs while maintaining security boundaries
- MCP Tunnels provide secure access to private Model Context Protocol servers without exposing them to the public internet
- Agent capabilities have progressed from simple test function generation to clearing entire development backlogs with merge-ready pull requests
