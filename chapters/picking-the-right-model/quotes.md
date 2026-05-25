# Notable quotes: Picking the right model

Quotes selected by Claude from the transcript.

> The key question often for you guys is, what does that mean for your use case? What does that mean for your business?

*Identifies the core problem that the talk aims to solve beyond marketing noise.*

> The model that's right for your use case is not necessarily the one that's cheapest or fastest per token, but the one that is cheapest per successful outcome.

*Central thesis of the talk that challenges conventional thinking about model selection.*

> A small. It can be a very small. Well-designed eval will be much more important for you guys to assess which model to use than any public benchmark out there.

*Core argument against relying on public benchmarks for production decisions.*

> When we actually dug into the transcripts, what we found was that Claude was going into the Git history and seeing what it did in previous trials and extracting the answer from there.

*Illustrates why examining transcripts is critical for understanding true model performance.*

> So prompt caching, we have a bunch of guides online and I would really encourage you to read into it more. But effectively, when you're using prompt caching and you're basically using a prefix of a prompt that's saved, precomputed, and precached, you pay one tenth the price of the list price of input tokens.

*Explains a key cost optimization technique that can dramatically change model economics.*

> My kind of hot take here is people spend too much time thinking about these super complex multi-agent orchestration systems and not enough time doing the simple thing that works, which is just good context hygiene and good context engineering.

*Advocates for focusing on fundamentals rather than complex architectures.*

> And in just cleaning up this response, we get a 66.4% reduction in tokens from this tool response. And that compounds every time, right?

*Demonstrates the compounding impact of context engineering optimizations.*

> So we're working on a web search use case with a customer. And we effectively deduplicated articles that were returned from the same search or from different searches, in fact. And this one trick, effectively, of multiple searches running, taking the articles and deduplicated them before they returned to Claude, led to a 77% reduction in the number of input tokens that Claude was receiving, a 65% reduction in cost, and Claude's accuracy actually went up 9%

*Provides concrete metrics showing how context engineering improves both cost and performance.*

> But it's only by digging into the transcripts that you start to see some of the actually underlying patterns that are emerging, some of the real things that need to be fixed and done.

*Emphasizes the importance of qualitative analysis alongside quantitative metrics.*

> And they actually decided to rerun the eval with Sonnet and Opus as well. And as you can see on the screen, they actually both scored 100% as well, but counterintuitively took way less time in doing so.

*Demonstrates the counterintuitive finding that larger models can be more efficient.*
