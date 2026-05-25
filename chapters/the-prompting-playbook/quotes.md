# Notable quotes: The prompting playbook

Quotes selected by Claude from the transcript.

> A general rule of thumb that I like to follow is if you're reading a prompt and you can't tell guidelines from policy from data, most likely the model isn't able to either.

*Provides a practical heuristic for prompt structure and clarity that directly impacts model performance.*

> Instructions don't add capability. Telling the model it's critical to do a calculation right doesn't make it better at mental maths.

*Key insight about the fundamental limitation of instructions versus providing actual tools and capabilities.*

> We worry a lot about hallucinations or the invention of facts and numbers. But actually the opposite can also happen. The model can withhold information that it actually has access to.

*Important counterintuitive observation about model behavior that challenges common assumptions about AI safety.*

> As models become more intelligent, we need to remember to state both sides of the trade-offs because our models are becoming better themselves at making those trade-offs themselves.

*Demonstrates how prompting strategies must evolve as model capabilities improve.*

> We need evaluations to provide that rigor to understand whether a change to a prompt is actually correlating to an improvement in its performance.

*Establishes the fundamental principle that systematic evaluation is required for effective prompt engineering.*

> Wherever we are making defensive changes in the prompt, we are tracking the reason why we've introduced these. Sometimes they're necessary, but in the future, these kind of changes can produce unwanted effects so that we can backtrack on them.

*Practical advice for version control and documentation in prompt engineering workflows.*

> So rather than using one prompt to address everything, we're actually isolating different tasks, where it's easy and repeatable to separate out the steps that it needs to take every time.

*Demonstrates the core principle behind effective agentic system design and task decomposition.*

> The new model might be capable, but it's behaving differently. And therefore, we can tune our prompting to fix that behavior. The second case is where actually the model that we're changing to isn't as capable, and no amount of prompting is going to fix that.

*Important distinction between behavioral differences and capability limitations when migrating between models.*

> You can put in soft requirements at runtime. So in the evaluation prompt we can say Harry doesn't like working with Sally so as much as possible try and separate them from working together.

*Illustrates the flexibility advantage of agentic approaches for handling dynamic requirements.*
