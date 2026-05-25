# Notable quotes: What legal agents inherit from coding agents: Lessons from Legora

Quotes selected by Claude from the transcript.

> We've all seen over the last years, AI and coding going from bad autocomplete to good autocomplete, chatbots, agents, and background agents and beyond.

*Captures the rapid evolution of AI capabilities in coding domain that other verticals are trying to catch up with.*

> Other verticals outside of coding are actually quite behind looking back like six months ago.

*Identifies the core motivation for the talk - the gap between coding AI progress and other domains.*

> Both coding and legal work are based heavily on prior work. Both lawyers and engineers work a lot with text-based documents. There are strict conventions within organizations and firms.

*Establishes the fundamental parallels between coding and legal work that enable pattern transfer.*

> There's basically three buckets how you can learn from coding agents as we found. First of all, there is stuff that you can reuse one to one. Stuff like to-dos, planning, sub-agents, sandboxes, human in the loop.

*Introduces the core framework for categorizing learnings from coding agents.*

> A docx file is basically a zip file of a bunch of XML files with a lot of metadata and a lot of noise in there. So, it's not as simple as like editing a markdown file.

*Explains the technical complexity that motivated their architectural choices for document editing.*

> What you have with this kind of setup is you have a lot of individual LLM calls with independent reasoning, different context, different tools. And you just have like all these handoff problems.

*Articulates the key problems with multi-model architectures that led to their redesign.*

> All the coding agents out there work in a way where they just read, edit, and verify things in a loop.

*Identifies the core pattern from coding agents that they successfully translated to legal document editing.*

> My mental model is kind of that you want to have the model almost feel like it's inside a coding agent harness. And it just does a legal task.

*Captures the key insight about leveraging existing training and optimization from coding agent development.*

> We passed the thing in. Asked the agent to translate paragraph by paragraph from English to Swedish. And just kept, like, started editing... And everything was translated. And the funniest part about this was that to test how good this, like, new harness and tool design works, we run this whole thing on Haiku.

*Demonstrates the effectiveness of their translated architecture even with smaller models.*

> It's basically ESLint for legal documents.

*Provides a clear analogy for how coding patterns translate to legal document validation.*
