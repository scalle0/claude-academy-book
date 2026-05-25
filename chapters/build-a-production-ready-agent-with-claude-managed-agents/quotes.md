# Notable quotes: Build a production-ready agent with Claude Managed Agents

Quotes selected by Claude from the transcript.

> Claude manage agents at a high level is just a set of API endpoints that we've developed and released. You can go use them with any API key today. That give you access to like scaled ready, production ready agents and all of the primitives around it that you can just build your own products on top of.

*Provides the core definition and value proposition of Claude Managed Agents as production-ready infrastructure*

> We took care of a lot of things like giving Claude access to a computer. Giving it access to credential vaults if you want to inject things like MCP authentication for your own end users.

*Highlights key infrastructure capabilities that developers get out of the box*

> You can also define certain permission controls on a per tool basis. So, you can decide that something like the file read tool can just auto execute, whereas something like executing bash or calling your database's MCP server requires explicit approval from the server.

*Demonstrates the granular security controls available for managing agent permissions*

> Since we announced self-hosted environments and sandboxes, you can also bring your own sandboxes through the environment. So, you can have your own sandboxes that don't just run on Anthropix infrastructure.

*Explains the flexibility of using custom infrastructure while maintaining the managed agent benefits*

> With credential vaults, we give Claude access to like one or several memory stores that it can then read and write memories from over time. So, that every session that it interacts with can like read from those previous memories and get better than the one before.

*Describes how persistent memory enables continuous learning and improvement across sessions*

> Without Claude ever seeing what those things are. Right. So, we make sure that like Claude, it never enters Claude's context window or anything like that. And makes the whole thing a lot more secure.

*Emphasizes the security design of credential management to protect sensitive authentication data*

> We use all of the Anthropic APIs. Specifically the managed agent APIs that we have. And that's really all you have to do to make Claude really, really good at using this thing.

*Shows how Claude Code includes built-in knowledge of Managed Agents APIs for self-building capabilities*

> With multiagent, Claude can like spin off individual threads of other agents. Kind of like what I showed earlier. So, there's a bunch of endpoints that are associated with that as well.

*Explains the multi-agent coordination capabilities and API structure*

> And use that in order to like have various agents with their own kind of personas and their own ways of doing things. So, maybe one agent is like in charge of figuring out macro trends in the overall. The overall industry that you're working with. Whereas another one is like really good at like financial analysis.

*Illustrates how different agents can be specialized for specific tasks within a coordinated workflow*

> If we were to do all of this by ourselves, we would have had to build our own agent loop or maybe use the agent SDK. Figure out a way to host it somewhere remote. Figure out things like context management and handling state transitions and recovery from those state transitions.

*Summarizes the complexity and infrastructure challenges that Managed Agents abstracts away for developers*
