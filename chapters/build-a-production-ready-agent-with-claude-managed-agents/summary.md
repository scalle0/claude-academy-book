# Summary: Build a production-ready agent with Claude Managed Agents

Chapter slug: `build-a-production-ready-agent-with-claude-managed-agents`

## Abstract

This talk provides a technical deep dive into Claude Managed Agents, a set of production-ready API endpoints that enable developers to build scalable agent applications without managing underlying infrastructure. The presentation covers the core primitives including agents, environments, sessions, and events, demonstrating how these components work together to create multi-agent systems. The speaker builds a live demo of a deal desk application that uses multiple specialized agents for financial analysis and company research. Key features discussed include self-hosted sandboxes, MCP tunnels for private data access, credential vaults for secure authentication, and memory stores for persistent knowledge. The system provides observability through a developer console for monitoring agent behavior and debugging sessions. Events are categorized into user events, agent events, session events, and span events, each serving specific purposes in the agent lifecycle. The platform handles tool calling, retries, error recovery, and multi-agent coordination automatically, allowing developers to focus on building product experiences rather than agent infrastructure.

## Key claims

- Claude Managed Agents provides production-ready API endpoints that handle agent infrastructure including sandboxing, tool calling, and error recovery
- The system supports self-hosted environments and MCP tunnels for connecting private data sources without exposing them to the internet
- Multi-agent coordination allows spawning specialized agents with different personas and tool access within a single session
- Credential vaults securely store MCP authentication tokens without exposing them to Claude's context window
- Memory stores enable agents to persist and retrieve knowledge across sessions for improved performance over time
- The developer console provides real-time observability and debugging capabilities for monitoring agent behavior
- Outcome events allow agents to iterate and self-evaluate their work against specified criteria until satisfactory results are achieved
