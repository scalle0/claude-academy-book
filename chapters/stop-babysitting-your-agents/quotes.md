# Notable quotes: Stop babysitting your agents

Quotes selected by Claude from the transcript.

> As models have been getting smarter, I've noticed that we're increasingly spending a larger percentage of our time staring at the screen, waiting for Claude to finish its work, or just acting as a glorified QA tester for Claude.

*Captures the core problem the talk aims to solve regarding inefficient human-AI collaboration patterns.*

> Most software tooling so far was built with humans in mind. Whether it's linters, IDEs, printers. I don't know. Either. Or μεs, IDEs, prettyers, type checkers, even compilers, they were mostly written with the goal of making humans and human teams faster.

*Establishes the fundamental mismatch between existing tools and AI agent needs.*

> what does an agent need from your code base that a human takes for granted?

*Key question that frames the entire approach to redesigning development workflows for AI agents.*

> A loop essentially is an autonomous circuit that you can complete for Claude, and it allows Claude, to hill climb on a given task or a given success criteria.

*Defines the core concept of verification loops that enables autonomous agent improvement.*

> You can think of a skill as just a way to store some arbitrary context about a specific topic. And in this case, that topic happens to be a verification loop.

*Explains how to package and distribute verification workflows as reusable components.*

> The interesting thing about skills also is that you can make them self-improving. So if you put in instructions into your skill about improving the skill every time Claude hits a blocker, you will end up creating this self-documenting, self-improving skill

*Describes a key capability for creating autonomous, evolving development tools.*

> I personally find that more than four to five sessions open simultaneously takes a big load on my brain. And I can't really function beyond that.

*Identifies human attention as the bottleneck in scaling AI-assisted development work.*

> remote control essentially gives you. The option to control any session running on any surface with your phone.

*Demonstrates how to decouple physical presence from AI agent management.*

> A lot of this is just bookkeeping in some ways. So personally, I'm spending a lot of my time now babysitting my PRs.

*Identifies common repetitive tasks that can be automated with background loops.*

> So slash loop is a way to run a prompt at a specific interval in Claude Code. So you can say slash loop 10 minutes. And babysit my open PRs.

*Shows the practical implementation of background automation for routine development tasks.*
