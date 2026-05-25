# Notable quotes: Memory and dreaming for self learning agents

Quotes selected by Claude from the transcript.

> Memory lets agents learn. It lets agents carry forward learnings from their previous tasks.

*Core definition of what memory accomplishes for agents in simple terms.*

> Models and Claude are great at navigating virtual environments and a file system. And Claude is also very capable at using familiar tools like Bash and grep to read, update, and organize files.

*Key technical insight behind the file system-based memory architecture design decision.*

> And so with memory, we've modeled it as a file system to Claude. Again, the key principle is getting out of Claude's way and letting it use the capabilities it already has.

*Design philosophy of leveraging existing model strengths rather than building new abstractions.*

> Rakuten saw a 97% decrease in first pass errors in agents deployed in production.

*Quantifiable production impact demonstrating the value of the memory system.*

> We call this process dreaming. And dreaming is available in Research Preview right now, and it can be used with managed agents. It's a process that looks for patterns and mistakes across agents and sessions.

*Introduction and definition of the dreaming capability.*

> Customers like Harvey saw a six times increase in completion rates for their legal benchmark with dreaming.

*Concrete performance improvement metric showing dreaming's effectiveness.*

> The out of band component of dreaming is really, really critical. Creating a process that's decoupled from the underlying agent loop has benefits.

*Important architectural decision explaining why dreaming runs separately from agent execution.*

> One way to think about dreaming is like thinking models or test time compute, where letting models spend some tokens to explore a problem, on average, produces better outcomes.

*Analogy connecting dreaming to broader AI concepts of computational investment for better results.*

> Dreaming itself is built on Claude managed agents. So it's a feature of Claude managed agents built on Claude managed agents itself.

*Technical detail showing the self-hosting nature of the dreaming system.*

> And continuously building upon and improving their understanding and view of the world around them is very critical to unlocking that capability.

*Vision statement about the importance of continuous learning for long-running agents.*
